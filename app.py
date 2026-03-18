# app.py
import streamlit as st
from pages_src.home import show_home
from pages_src.quiz import show_quiz

# ================================
# Configurações gerais do app
# ================================
st.set_page_config(
    page_title="Quiz Kids",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================
# Menu lateral simples
# ================================
pagina = st.sidebar.radio(
    "Escolha a página:",
    ["🏠 Home", "Matemática"]
)

# ================================
# Renderizar página selecionada
# ================================
if pagina == "🏠 Home":
    show_home()
else:
    show_quiz(pagina)