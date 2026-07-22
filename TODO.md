# TODO
- [x] Fix Streamlit session_state KeyError by using `login_type` consistently in `app.py` (instead of `login_state`).- [x] Confirm root cause of face-recognition failure: missing pkg_resources from setuptools in the project venv breaks the face_recognition_models import path.
- [x] Repair the environment by reinstalling a setuptools version that still provides pkg_resources and reinstalling the requirements.- [ ] Make voice pipeline robust when optional voice deps (resemblyzer/webrtcvad) are not installed (Windows/MSVC issues).
  - [x] Replace placeholder voice_pipeline.py with optional-dependency guarded implementation.
  - [ ] Update screens to call voice pipeline only when `voice_features_available()` is True.
  - [ ] Adjust requirements.txt (pin/add platform markers) or document MSVC requirement.

