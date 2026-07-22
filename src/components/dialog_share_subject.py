import streamlit as st
import segno
import io

@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    st.markdown(
        """
        <style>
        div[data-testid="stDialogHeader"] h1, 
        div[data-testid="stDialogHeader"] h2,
        div[data-testid="stDialogHeader"] button {
            color: #FFFFFF !important;
        }
        
        div[data-testid="stDialog"] h1, 
        div[data-testid="stDialog"] h2 {
            color: #FFFFFF !important;
            font-family: 'Outfit', sans-serif !important;
        }

        div[role="dialog"] div.share-card-text,
        div[role="dialog"] div.share-card-text *,
        div[data-testid="stDialog"] div.share-card-text,
        div[data-testid="stDialog"] div.share-card-text * {
            color: #000000 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    app_domain = "DeProxy-main.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.header("Scan to join")

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=1)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<h3 style="font-family: \'Outfit\', sans-serif; color: #FFFFFF !important;">Copy Link</h3>', unsafe_allow_html=True)
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        
        st.markdown('<div class="share-card-text" style="font-family: \'Outfit\', sans-serif; background-color: #FFFFFF; padding: 12px; border-radius: 0.5rem; border: 1px solid #E0E3FF; margin-top: 8px; font-weight: 500;">Copy this link to share</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<h3 style="font-family: \'Outfit\', sans-serif; color: #FFFFFF !important;">Scan to join</h3>', unsafe_allow_html=True)
        st.image(out.getvalue(), caption='Join class via QR-CODE')