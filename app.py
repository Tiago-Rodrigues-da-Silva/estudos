# app.py

import streamlit as st
from pages.home import show_home
from pages.quiz import show_quiz
from utils.style import apply_responsive_style

# Aplica o CSS responsivo (desktop e mobile com botão menu)
apply_responsive_style()

# Configuração da página
st.set_page_config(
    page_title="Quiz Kids",
    page_icon="⭐",
    layout="wide"
)

# Título do sidebar
st.sidebar.title("Menu")

# Menu de seleção de página
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

# Renderiza a página selecionada
if pagina == "🏠 Home":
    show_home()
else:
    show_quiz(pagina)