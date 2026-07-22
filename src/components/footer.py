import streamlit as st


def footer_home():
    st.markdown(
        """
        <div style="margin-top:2rem; padding-bottom:1rem; display:flex; justify-content:center; align-items:center;">
            <p style="margin:0; color:white; font-size:2.3rem; font-weight:600; letter-spacing:0.02em; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Developed by Satyam</p>
        </div>
        """,
        unsafe_allow_html=True,
    )