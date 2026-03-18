# services/google_sheets.py
import os
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

def carregar_questoes(nome_planilha):
    """
    Carrega questões do Google Sheets.
    - Usa Streamlit Secrets se estiver no Cloud
    - Usa credentials.json se estiver local
    """
    creds = None

    # Tenta usar Streamlit Secrets (apenas se existir)
    try:
        import streamlit as st
        # Tenta acessar o secret; se não existir, gera exceção
        cred_dict = dict(st.secrets["gcp_service_account"])
        cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
        creds = Credentials.from_service_account_info(
            cred_dict,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
        )
    except (ModuleNotFoundError, KeyError, st.errors.StreamlitSecretNotFoundError):
        # fallback para localhost
        json_path = os.path.join(os.getcwd(), "credentials.json")
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {json_path}")
        creds = Credentials.from_service_account_file(
            json_path,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
        )

    client = gspread.authorize(creds)
    sheet = client.open(nome_planilha)
    worksheet = sheet.sheet1
    dados = worksheet.get_all_records()
    df = pd.DataFrame(dados)
    return df