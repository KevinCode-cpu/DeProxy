import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f'<div style="background-color: #FFFFFF; border-left: 8px solid #EB459E; padding: 25px; padding-bottom: 10px; border-radius: 20px; border: 1px solid #000000; width: 100%; box-sizing: border-box; margin-bottom: 30px;"><h3 style="margin: 0; color: #1e293b; font-size: 1.5rem;">{name}</h3><p style="color: #64748b; margin: 10px 0;">Code : <span style="background: #E0E3FF; color: #5865F2; padding: 2px 8px; border-radius: 5px;"> {code} </span> | Section : {section}</p>'
    
    if stats:
        html += '<div style="display: flex; gap: 8px; flex-wrap: wrap;">'
        for icon, label, value in stats:
            html += f'<div style="background-color: #FCE7F3; padding: 6px 12px; border-radius: 12px; font-size: 0.9rem;"><span style="color: #000000;">{icon}</span> <strong style="color: #000000;">{value}</strong> <span style="color: #000000;">{label}</span></div>'
        html += '</div>'

    html += '</div>'

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
