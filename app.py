import streamlit as st
from pages.home import show_home
from pages.quiz import show_quiz
from utils.style import hide_streamlit_menu

hide_streamlit_menu()

st.set_page_config(

    page_title="Quiz Kids",
    page_icon="⭐",
    layout="wide"

)

st.sidebar.title("Menu")

pagina=st.sidebar.radio(

"Escolha",

[

"🏠 Home",
"Português",
"Matemática",
"Geografia",
"História"

]

)

if pagina=="🏠 Home":

    show_home()

else:

    show_quiz(pagina)