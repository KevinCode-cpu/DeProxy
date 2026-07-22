import base64
from pathlib import Path

import streamlit as st


def header_home():
    logo_path = Path(__file__).resolve().parent / "logo (2).png"
    encoded_logo = base64.b64encode(logo_path.read_bytes()).decode("utf-8")

    st.markdown(
        f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:20px; margin-top:20px">
            <img src="data:image/png;base64,{encoded_logo}" style="height:70px; width:70px; object-fit:cover; border-radius:20%; border:2px solid #d0d7de;" />
            <h1 style='text-align:center; color:black; font-size:2rem; margin:8px 0 0 0;'>DeProxy</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

def header_dashboard():
        logo_path = Path(__file__).resolve().parent / "logo (2).png"
        encoded_logo = base64.b64encode(logo_path.read_bytes()).decode("utf-8")

        st.markdown(
          f"""
           <div style="display:flex; align-items:center; justify-content:center; gap:10px; margin-bottom:20px; margin-top:20px">
            <img src="data:image/png;base64,{encoded_logo}" style="height:70px; width:70px; object-fit:cover; border-radius:20%; border:2px solid #d0d7de;" />
            <h2 style='text-align:left; color:#5865F2; font-size:2rem; margin:8px 0 0 0;'>DeProxy</h1>
          </div>
           """,
            unsafe_allow_html=True,
        )