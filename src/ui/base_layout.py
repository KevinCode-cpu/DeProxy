import streamlit as st


def style_background_home():

    st.markdown("""
       <style>
                 
            .stApp {
                background:  #E865F2 !important
                }
            .stApp div[data-testid="stColumn"]{
                background-color:#E0E3FF !important;
                padding:2.5rem !important;
                border-radius: 5rem !important;
                }
       </style>                  
                
                """
                ,unsafe_allow_html=True)
    
def style_background_dashboard():

    st.markdown("""
       <style>
                 
                .stApp {
                background:  #E865F2 !important
                }

       </style>                  
                
                """
                ,unsafe_allow_html=True)

def style_base_layout():

    st.markdown("""
        <style>
                
          @import url('https://fonts.googleapis.com/css2?family=Ribeye&display=swap');     
          @import url('https://fonts.googleapis.com/css2?family=Crete+Round:ital@0;1&display=swap');  
                
         h1 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 3.5rem !important;   
            line-height:1.1 !important;
            margin-bottom:0rem !important;    
            }    
                
         h2 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 2rem !important;   
            line-height:0.9 !important;
            margin-bottom:0rem !important;    
            color: black !important;
            } 
                
         h3, h4, p {
            font-family: 'Outfit', sans-serif !important;
            }

         /* =========================================================
            BUTTON STYLING & WHITE TEXT FIX
            ========================================================= */
         div.stButton > button {
            background-color: #5865F2 !important;
            border-radius: 1.5rem !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out, background-color 0.25s ease-in-out !important;
            cursor: pointer !important;
            }

         div.stButton > button *,
         div.stButton > button p,
         div.stButton > button span {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
            }

         div.stButton > button[kind="secondary"] {
            background-color: #EB459E !important;
            }

         div.stButton > button[kind="tertiary"] {
            background-color: black !important;
            }

         div.stButton > button:hover {
            transform: scale(1.05) !important;
            }

         /* =========================================================
            DIALOG / POPUP MODAL FIX (FORCE ALL MODAL TEXT TO WHITE)
            ========================================================= */
         div[role="dialog"] *,
         div[data-testid="stDialog"] *,
         div[role="dialog"] h1,
         div[role="dialog"] h2,
         div[role="dialog"] h3,
         div[role="dialog"] p,
         div[role="dialog"] span,
         div[role="dialog"] label {
            color: #FFFFFF !important;
            }

         /* Keep input text readable inside input fields */
         div[role="dialog"] input {
            color: #FFFFFF !important;
            background-color: #1F2937 !important;
            }
     
        </style>                  
                
        """, unsafe_allow_html=True)