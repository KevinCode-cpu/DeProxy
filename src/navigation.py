"""Navigation helpers for in-app back navigation.

Provides:
- Back button on every non-home page (top-left via Streamlit col layout)
- Phone hardware back button support (via query param JS interception)
- Navigation history stack tracking
"""

import streamlit as st


def capture_state():
    """Capture the current full navigation state as a dictionary."""
    state = {
        'login_type': st.session_state.get('login_type', None),
        'teacher_login_type': st.session_state.get('teacher_login_type', 'login'),
        'is_logged_in': st.session_state.get('is_logged_in', False),
        'user_role': st.session_state.get('user_role', None),
        'has_teacher_data': 'teacher_data' in st.session_state,
        'has_student_data': 'student_data' in st.session_state,
        'current_teacher_tab': st.session_state.get('current_teacher_tab', 'take_attendance'),
    }
    # Deep-copy the teacher_data if present
    if 'teacher_data' in st.session_state:
        state['teacher_data'] = dict(st.session_state.teacher_data)
    else:
        state['teacher_data'] = None
    # Deep-copy the student_data if present
    if 'student_data' in st.session_state:
        state['student_data'] = dict(st.session_state.student_data)
    else:
        state['student_data'] = None
    return state


def restore_state(state):
    """Restore full session state from a previously captured state dict."""
    st.session_state.login_type = state.get('login_type')
    st.session_state.teacher_login_type = state.get('teacher_login_type', 'login')
    st.session_state.is_logged_in = state.get('is_logged_in', False)
    st.session_state.user_role = state.get('user_role', None)

    if state.get('current_teacher_tab'):
        st.session_state.current_teacher_tab = state['current_teacher_tab']

    # Restore teacher_data
    if state.get('has_teacher_data') and state.get('teacher_data'):
        st.session_state.teacher_data = state['teacher_data']
    elif 'teacher_data' in st.session_state and not state.get('has_teacher_data'):
        del st.session_state.teacher_data

    # Restore student_data
    if state.get('has_student_data') and state.get('student_data'):
        st.session_state.student_data = state['student_data']
    elif 'student_data' in st.session_state and not state.get('has_student_data'):
        del st.session_state.student_data


def get_screen_name():
    """Return a human-readable screen name for the current state."""
    lt = st.session_state.get('login_type', None)
    if lt is None:
        return 'home'
    if lt == 'teacher':
        if st.session_state.get('teacher_data'):
            return 'teacher_dashboard'
        tlt = st.session_state.get('teacher_login_type', 'login')
        return f'teacher_{tlt}'
    if lt == 'student':
        if st.session_state.get('student_data'):
            return 'student_dashboard'
        return 'student_login'
    return 'home'


def is_home():
    """Check if currently on the home screen."""
    return get_screen_name() == 'home'


def setup_navigation():
    """Initialize nav history on first run and handle back navigation.

    Must be called at the very top of main(), before any other UI is rendered.
    """
    # Ensure nav_history exists
    if 'nav_history' not in st.session_state:
        st.session_state.nav_history = []
        st.session_state._nav_initialized = False

    # Track back-navigation flag
    if '_is_back_nav' not in st.session_state:
        st.session_state._is_back_nav = False

    # ── Handle hardware back button (phone) via query param ──
    if st.query_params.get('_dpback') == '1':
        # Remove only _dpback, not other params like join-code
        st.query_params.pop('_dpback', None)
        _perform_back()
        st.rerun()

    # ── Track forward navigation ──
    current_state = capture_state()
    current_screen = get_screen_name()
    prev_state = st.session_state.get('_prev_captured_state')
    prev_screen = st.session_state.get('_prev_screen')

    if (
        prev_state is not None
        and prev_screen is not None
        and prev_screen != current_screen
        and not st.session_state._is_back_nav
    ):
        # User navigated forward — save previous state to history
        st.session_state.nav_history.append(prev_state)

    # Reset back-nav flag after one cycle
    st.session_state._is_back_nav = False
    # Store for next comparison
    st.session_state._prev_captured_state = current_state
    st.session_state._prev_screen = current_screen


def _perform_back():
    """Pop nav history and restore state (internal)."""
    if st.session_state.nav_history:
        target = st.session_state.nav_history.pop()
        st.session_state._is_back_nav = True
        restore_state(target)


def go_back():
    """Public function: navigate one step back in the app."""
    _perform_back()
    st.rerun()


def inject_back_button_js():
    """Inject JavaScript to intercept the phone's hardware back button.

    Uses the `<img onerror="...">` trick (since Streamlit strips <script> tags).
    The onerror event fires because the image source "x" fails to load.
    """
    st.markdown(
        '<img src="x" onerror="'
        '(function(){'
        'if(window._dpNavInitialized)return;'
        'window._dpNavInitialized=true;'
        'var inBack=false;'
        'window.addEventListener(\'popstate\',function(e){'
        'if(inBack)return;inBack=true;'
        'var url=new URL(window.location);'
        'url.searchParams.set(\'_dpback\',\'1\');'
        'window.location.href=url.toString();'
        '});'
        'window.history.pushState(null,\'\',window.location.href);'
        '})()" '
        'style="display:none" />',
        unsafe_allow_html=True,
    )


def render_back_button():
    """Render a small '←' back button at the top-left of non-home pages.

    Uses a Streamlit columns layout with the back button as the first element.
    """
    if is_home():
        return  # No back button on the home screen

    # Use a narrow column for the back button, then let content flow naturally
    back_col, _ = st.columns([0.08, 0.92])
    with back_col:
        if st.button("←", key="_dp_back_btn", help="Go back"):
            go_back()

