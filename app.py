# app.py

import streamlit as st

# Importar páginas
from pages.home import show_home
from pages.quiz import show_quiz

# Importar estilo responsivo
from utils.style import apply_responsive_style

# Aplicar CSS responsivo (desktop e mobile)
apply_responsive_style()

# Configuração da página
st.set_page_config(
    page_title="Quiz Kids",
    page_icon="⭐",
    layout="wide"
)

# Sidebar / Menu lateral
st.sidebar.title("Menu")
pagina = st.sidebar.radio(
    "Escolha",
    [
        "🏠 Home",
        "Português",
        "Matemática",
        "Geografia",
        "História"
    ]
)

# Renderização das páginas
if pagina == "🏠 Home":
    show_home()
else:
    show_quiz(pagina)