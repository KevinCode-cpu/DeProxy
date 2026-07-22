import streamlit as st

# Heavy face-recognition imports are intentionally delayed/guarded.
# This prevents Streamlit from crashing at import-time on environments
# that cannot install native deps (e.g., dlib/face_recognition_models).

import numpy as np
from sklearn.svm import SVC

from src.database.db import get_all_students


def _import_face_deps():
    """Import heavy face-recognition deps on-demand.

    This function raises only for hard developer errors.
    Missing runtime deps should be handled gracefully by callers.
    """
    try:
        import dlib
        import face_recognition_models
    except ModuleNotFoundError as e:
        # Common case: setuptools installation is broken/missing pkg_resources.
        missing = str(e)
        if "pkg_resources" in missing or "setuptools" in missing:
            raise RuntimeError(
                "Face recognition deps are installed incorrectly: missing 'pkg_resources' (from setuptools). "
                "Reinstall setuptools cleanly (or recreate venv) and then reinstall dlib/face_recognition_models. "
                f"Root cause: {e}"
            ) from e
        raise RuntimeError(
            "Face recognition dependencies are not available. "
            "Install/enable 'dlib' and 'face_recognition_models' (via requirements.txt) "
            f"and ensure native build dependencies are satisfied. Missing: {e}"
        ) from e
    except Exception as e:
        raise RuntimeError(
            "Face recognition dependencies are not available. "
            "Install/enable 'dlib' and 'face_recognition_models' (via requirements.txt) "
            "and ensure native build dependencies are satisfied. "
            f"Root cause: {e}"
        ) from e
    return dlib, face_recognition_models




@st.cache_resource
def load_dlib_models():
    """Load dlib face detector + predictors.

    If dependencies are missing, return None values so the app can keep running
    (face recognition features will be disabled).
    """
    try:
        dlib, face_recognition_models = _import_face_deps()

        detector = dlib.get_frontal_face_detector()
        sp = dlib.shape_predictor(
            face_recognition_models.pose_predictor_model_location()
        )
        facerec = dlib.face_recognition_model_v1(
            face_recognition_models.face_recognition_model_location()
        )

        return detector, sp, facerec
    except Exception as e:
        st.warning(f"Face recognition disabled: {e}")
        return None, None, None



def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    if detector is None or sp is None or facerec is None:
        return []

    faces = detector(image_np, 1)

    encodings = []
    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
        encodings.append(np.array(face_descriptor))
    return encodings



@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()
    if not student_db:
        return None

    for student in student_db:
        embedding = student.get("face_embedding")
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get("student_id"))

    if len(X) == 0:
        return 0

    clf = SVC(kernel="linear", probability=True, class_weight="balanced")

    try:
        clf.fit(X, y)
    except ValueError:
        pass

    return {"clf": clf, "X": X, "y": y}


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)

    detected_student = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_student, [], len(encodings)

    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(list(set(y_train)))

    last_len = len(encodings)
    for encoding in encodings:
        if len(all_students) >= 2:
            predicted_id = int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])

        student_embedding = X_train[y_train.index(predicted_id)]

        best_match_score = np.linalg.norm(student_embedding - encoding)

        resemblance_threshold = 0.6

        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True

    return detected_student, all_students, last_len

