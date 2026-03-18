# style.py

import streamlit as st

def apply_responsive_style():
    st.markdown("""
    <style>
    /* Esconder menu/header/footer padrão */
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    
    /* Mostrar sidebar lateral */
    [data-testid="stSidebarNav"] {display:block !important;}
    </style>
    """, unsafe_allow_html=True)