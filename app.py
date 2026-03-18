# app.py
import streamlit as st
from utils.style import hide_streamlit_menu

# ================================
# Configurações gerais do app
# ================================
hide_streamlit_menu()  # esconde menu do Streamlit, header e footer

st.set_page_config(
    page_title="Quiz Kids",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={  # Remove opções do menu padrão
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# ================================
# Menu lateral customizado
# ================================
st.sidebar.title("Menu")
pagina = st.sidebar.radio(
    "Escolha a página:",
    [
        "🏠 Home",
        "Português",
        "Matemática",
        "Geografia",
        "História"
    ]
)

# ================================
# Importar páginas (agora sem usar 'pages/')
# ================================
# Renomeie sua pasta 'pages/' para 'pages_src/' ou similar
from pages_src.home import show_home
from pages_src.quiz import show_quiz

# ================================
# Renderizar página selecionada
# ================================
if pagina == "🏠 Home":
    show_home()
else:
    show_quiz(pagina)