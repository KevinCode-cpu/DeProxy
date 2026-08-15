from src.database.config import supabase, SUPABASE_URL

import bcrypt


def _raise_supabase_auth_error(exc):
    raise RuntimeError(
        "Supabase authentication failed: check that SUPABASE_URL and SUPABASE_SECRET_KEY belong to the same project and are not stale or mismatched. "
        "Update streamlit/secrets.toml or your environment variables with a valid key."
    ) from exc


def _execute_supabase(callable_obj):
    if supabase is None:
        raise RuntimeError(
            "Supabase client is not configured. Fix .streamlit/secrets.toml or set SUPABASE_URL and SUPABASE_SECRET_KEY env vars."
        )

    try:
        return callable_obj()
    except Exception as exc:
        message = str(exc)
        if "Unregistered API key" in message or "JSON could not be generated" in message or "401" in message:
            _raise_supabase_auth_error(exc)
        raise


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()


def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    return _execute_supabase(
        lambda: len(supabase.table("teachers").select("username").eq("username", username).execute().data) > 0
    )


def create_teacher(username, password, name):
    data = {"username": username, "password": hash_pass(password), "name": name}
    return _execute_supabase(lambda: supabase.table("teachers").insert(data).execute())


def teacher_login(username, password):
    response = _execute_supabase(lambda: supabase.table("teachers").select("*").eq("username", username).execute())
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None


def get_all_students():
    response = _execute_supabase(lambda: supabase.table('students').select("*").execute())
    return response.data


def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding': face_embedding, 'voice_embedding': voice_embedding}
    response = _execute_supabase(lambda: supabase.table('students').insert(data).execute())
    return response.data


def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = _execute_supabase(lambda: supabase.table("subjects").insert(data).execute())
    return response.data


def get_teacher_subjects(teacher_id):
    response = _execute_supabase(
        lambda: supabase.table('subjects').select("*, subject_students(count), attendance_logs(time_stamp)").eq("teacher_id", teacher_id).execute()
    )
    subjects = response.data

    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['time_stamp'] for log in attendance))
        sub['total_classes'] = unique_sessions

        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects


def enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    response = _execute_supabase(lambda: supabase.table('subject_students').insert(data).execute())
    return response.data


def unenroll_student_to_subject(student_id, subject_id):
    response = _execute_supabase(lambda: supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute())
    return response.data


def get_student_subjects(student_id):
    response = _execute_supabase(lambda: supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute())
    return response.data


def get_student_attendance(student_id):
    response = _execute_supabase(lambda: supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute())
    return response.data


def create_attendance(logs):
    response = _execute_supabase(lambda: supabase.table('attendance_logs').insert(logs).execute())
    return response.data


def get_attendance_for_teacher(teacher_id):
    response = _execute_supabase(lambda: supabase.table('attendance_logs').select("*, subjects! inner(*)").eq('subjects.teacher_id', teacher_id).execute())
    return response.data
