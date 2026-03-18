# services/resultado_service.py
import os
from datetime import datetime
import pytz

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

# -----------------------------
# Conexão com Google Sheets
# -----------------------------
def conectar():
    """
    Conecta ao Google Sheets usando:
    - 'credentials.json' no desenvolvimento local
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
    # ⭐ Streamlit Cloud
    elif "gcp_service_account" in st.secrets:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        ).with_scopes(scope)
    else:
        st.error("⚠️ Credenciais não encontradas! Coloque 'credentials.json' local ou configure 'st.secrets'.")
        return None  # retorna None em vez de quebrar o app

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
    if client is None:
        st.warning("Não foi possível salvar. Credenciais ausentes.")
        return

    try:
        sheet = client.open("resultados_quiz")
        worksheet = sheet.sheet1

        fuso_brasilia = pytz.timezone("America/Sao_Paulo")

        nova_linha = [
            nome,
            materia,
            float(nota),  # sempre número real
            datetime.now(fuso_brasilia).strftime("%d/%m/%Y %H:%M")  # horário de Brasília
        ]

        worksheet.append_row(nova_linha)
        st.success("Resultado salvo com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar resultado: {e}")

# -----------------------------
# Carregar resultados
# -----------------------------
def carregar_resultados() -> pd.DataFrame:
    """
    Retorna um DataFrame com todos os resultados do Sheet.
    Faz normalização robusta da coluna 'Nota'.
    """
    client = conectar()
    if client is None:
        return pd.DataFrame()  # retorna vazio se não tiver credenciais

    try:
        sheet = client.open("resultados_quiz")
        worksheet = sheet.sheet1

        dados = worksheet.get_all_records()
        df = pd.DataFrame(dados)

        if df.empty:
            return df

        # ⭐ Normalização robusta da nota
        if 'Nota' in df.columns:
            df['Nota'] = df['Nota'].astype(str)
            df['Nota'] = df['Nota'].str.replace(",", ".", regex=False)
            df['Nota'] = pd.to_numeric(df['Nota'], errors='coerce')

            # Proteção contra notas >10 (ex: 240 -> 2.4)
            if df['Nota'].max() > 10:
                df['Nota'] = df['Nota'] / 100

        return df
    except Exception as e:
        st.error(f"Erro ao carregar resultados: {e}")
        return pd.DataFrame()