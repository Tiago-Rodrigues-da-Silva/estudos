def hide_streamlit_menu():

    import streamlit as st

    st.markdown("""

<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

[data-testid="stSidebarNav"] {

display:none;

}

</style>

""", unsafe_allow_html=True)