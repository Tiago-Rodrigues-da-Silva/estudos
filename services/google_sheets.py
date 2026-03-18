# services/google_sheets.py
import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

def carregar_questoes(nome_planilha):
    # Criar cópia mutável do secret
    cred_dict = dict(st.secrets["gcp_service_account"])

    # Corrigir quebras de linha
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(cred_dict, scopes=scope)
    client = gspread.authorize(creds)

    sheet = client.open(nome_planilha)
    worksheet = sheet.sheet1
    dados = worksheet.get_all_records()
    df = pd.DataFrame(dados)

    return df