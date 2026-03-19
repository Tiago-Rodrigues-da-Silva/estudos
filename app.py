# app.py

import streamlit as st
from services.auth_service import autenticar
from pages_src.home import show_home
from pages_src.quiz import show_quiz

# ================================
# Configuração (SEMPRE PRIMEIRO)
# ================================
st.set_page_config(

    page_title="Simulado 6º ano",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded"

)

# ================================
# LOGIN
# ================================
def login():

    st.title("🎓 Simulado 6º ano")

    st.subheader("Login")

    usuario = st.text_input("Usuário")

    senha = st.text_input(
        "Senha",
        type="password"
    )

    if st.button("Entrar"):

        nome = autenticar(
            usuario,
            senha
        )

        if nome:

            st.session_state.logado = True

            st.session_state.usuario = usuario   # ⭐ faltava
            st.session_state.nome = nome

            st.rerun()

        else:

            st.error(
                "Usuário ou senha inválidos"
            )

# se não logado
if "logado" not in st.session_state:

    login()

    st.stop()

# ================================
# SIDEBAR
# ================================
st.sidebar.write(
    f"👤 {st.session_state.nome}"
)

if st.sidebar.button("Logout"):

    st.session_state.clear()

    st.rerun()

pagina = st.sidebar.radio(

    "Escolha:",

    [

        "🏠 Home",

        "Matemática",

        "Português",

        "Espanhol"

    ]

)

# ================================
# PÁGINAS
# ================================
if pagina == "🏠 Home":

    show_home()

else:

    show_quiz(pagina)