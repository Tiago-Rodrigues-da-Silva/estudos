# google_sheets.py
import json
import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

def carregar_questoes(nome_planilha):
    # Ler credenciais do Streamlit Secrets
    cred_dict = st.secrets["gcp_service_account"]

    # Converter o private_key de múltiplas linhas
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")

    # Escopos necessários
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        cred_dict,
        scopes=scope
    )

    client = gspread.authorize(creds)
    sheet = client.open(nome_planilha)
    worksheet = sheet.sheet1
    dados = worksheet.get_all_records()
    df = pd.DataFrame(dados)

    return df