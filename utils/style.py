# style.py

import streamlit as st

def apply_responsive_style():
    """
    Aplica CSS responsivo ao app Streamlit.
    - Desktop: esconde menu, header, footer e sidebar
    - Mobile: mostra menu, header e footer, transforma sidebar em botão de menu
    """
    st.markdown("""
    <style>
    /* =========================
       Desktop (>=768px) - esconder tudo
       ========================= */
    @media (min-width: 768px) {
        #MainMenu {visibility:hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}
        [data-testid="stSidebarNav"] {display:none;}
    }

    /* =========================
       Mobile (<768px) - menu visível, sidebar botão
       ========================= */
    @media (max-width: 767px) {
        #MainMenu {visibility:visible;}
        footer {visibility:visible;}
        header {visibility:visible;}

        /* Sidebar inicialmente escondida */
        [data-testid="stSidebarNav"] {
            display:none;
        }

        /* Botão "Menu" fixo no topo esquerdo */
        .mobile-menu-btn {
            position: fixed;
            top: 10px;
            left: 10px;
            background-color: #1f77b4;
            color: white;
            padding: 8px 12px;
            border-radius: 5px;
            z-index: 9999;
            cursor: pointer;
            font-weight: bold;
            font-family: sans-serif;
        }
    }
    </style>

    <!-- Botão "Menu" para mobile -->
    <div class="mobile-menu-btn" onclick="
        const sidebar = document.querySelector('[data-testid=stSidebarNav]');
        if (sidebar.style.display === 'block') { sidebar.style.display = 'none'; } 
        else { sidebar.style.display = 'block'; }
    ">☰ Menu</div>
    """, unsafe_allow_html=True)