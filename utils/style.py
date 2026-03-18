# utils/style.py
import streamlit as st

def hide_streamlit_menu():
    st.markdown(
        """
        <style>
        /* Esconde menu de hamburger / menu do diretório pages */
        #MainMenu {visibility: hidden;}
        /* Esconde rodapé padrão do Streamlit */
        footer {visibility: hidden;}
        /* Esconde cabeçalho Streamlit */
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )