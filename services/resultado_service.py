# services/resultado_service.py
import gspread
import pandas as pd
import streamlit as st
import os
from datetime import datetime
from google.oauth2.service_account import Credentials

# -----------------------------
# Conexão com Google Sheets
# -----------------------------
def conectar():
    """
    Conecta ao Google Sheets usando:
    - arquivo local 'credentials.json' no desenvolvimento
    - st.secrets['gcp_service_account'] no Streamlit Cloud
    """
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # ⭐ Desenvolvimento local
    if os.path.exists("credentials.json"):
        creds = Credentials.from_service_account_file(
            "credentials.json",
            scopes=scope
        )
    # ⭐ Produção / Streamlit Cloud
    elif "gcp_service_account" in st.secrets:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        ).with_scopes(scope)
    else:
        raise FileNotFoundError(
            "Credenciais não encontradas! Coloque 'credentials.json' ou configure 'st.secrets'."
        )

    client = gspread.authorize(creds)
    return client

# -----------------------------
# Salvar resultado no Sheet
# -----------------------------
def salvar(nome: str, materia: str, nota):
    """
    Salva uma linha de resultado no Google Sheet.
    """
    client = conectar()
    sheet = client.open("resultados_quiz")
    worksheet = sheet.sheet1

    nova_linha = [
        nome,
        materia,
        float(nota),  # sempre número real
        datetime.now().strftime("%d/%m/%Y %H:%M")
    ]

    worksheet.append_row(nova_linha)

# -----------------------------
# Carregar resultados
# -----------------------------
def carregar_resultados() -> pd.DataFrame:
    """
    Retorna um DataFrame com todos os resultados do Sheet.
    Faz normalização robusta da coluna 'Nota'.
    """
    client = conectar()
    sheet = client.open("resultados_quiz")
    worksheet = sheet.sheet1

    dados = worksheet.get_all_records()
    df = pd.DataFrame(dados)

    if df.empty:
        return df

    # ⭐ normalização robusta da nota
    if 'Nota' in df.columns:
        df['Nota'] = df['Nota'].astype(str)
        df['Nota'] = df['Nota'].str.replace(",", ".", regex=False)
        df['Nota'] = pd.to_numeric(df['Nota'], errors='coerce')

        # proteção bug notas >10 (ex: 240 -> 2.4)
        if df['Nota'].max() > 10:
            df['Nota'] = df['Nota'] / 100

    return df