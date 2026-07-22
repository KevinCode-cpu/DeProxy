import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.components.dialog_auto_enroll import auto_enroll_dialog
from src.navigation import (
    setup_navigation,
    inject_back_button_js,
    render_back_button,
)

def main():
   st.set_page_config(
      page_title='DeProxy - No more recalling for attendance',
      page_icon="logo (2).png"
   )

   # Initialize navigation history and handle hardware back button
   setup_navigation()

   # Inject JavaScript to intercept phone back button
   inject_back_button_js()

   # Ensure login_type exists in session state
   if 'login_type' not in st.session_state:
      st.session_state['login_type'] = None

   # Render a visible back button on every page except home
   render_back_button()

   match st.session_state['login_type']:
      case 'teacher':
         teacher_screen()

      case 'student':
         student_screen()

      case None:
         home_screen()

   join_code = st.query_params.get('join-code')
   if join_code:
      if st.session_state.login_type != 'student':
         st.session_state.login_type = 'student'
         st.rerun()
      if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
         auto_enroll_dialog(join_code)

main()

