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
def salvar(usuario: str, nome: str, materia: str, nota):

    client = conectar()

    if client is None:
        st.warning("Não foi possível salvar. Credenciais ausentes.")
        return

    try:

        sheet = client.open("resultados_quiz")

        worksheet = sheet.sheet1

        fuso_brasilia = pytz.timezone("America/Sao_Paulo")

        nova_linha = [

            usuario,   # ⭐ apenas adicionado
            nome,
            materia,
            float(nota),

            datetime.now(fuso_brasilia).strftime(
                "%d/%m/%Y %H:%M"
            )

        ]

        worksheet.append_row(nova_linha)

        st.success("Resultado salvo com sucesso!")

    except Exception as e:

        st.error(f"Erro ao salvar resultado: {e}")

# -----------------------------
# Carregar resultados
# -----------------------------
def carregar_resultados(usuario=None) -> pd.DataFrame:

    client = conectar()

    if client is None:
        return pd.DataFrame()

    try:

        sheet = client.open("resultados_quiz")

        worksheet = sheet.sheet1

        # ⭐ CORREÇÃO REAL
        dados = worksheet.get_all_values()

        df = pd.DataFrame(
            dados[1:],
            columns=dados[0]
        )

        # ⭐ necessário no cloud
        df.columns = df.columns.str.strip()

        df = df.astype(str)

        if df.empty:
            return df

        # ⭐ filtro correto
        if usuario and 'Usuario' in df.columns:

            usuario = str(usuario).strip()

            df['Usuario'] = df[
                'Usuario'
            ].astype(str).str.strip()

            df = df[
                df['Usuario'] == usuario
            ]

        # normalização nota
        if 'Nota' in df.columns:

            df['Nota'] = df['Nota'].str.replace(",", ".")

            df['Nota'] = pd.to_numeric(
                df['Nota'],
                errors='coerce'
            )

            if df['Nota'].max() > 10:

                df['Nota'] = df['Nota'] / 100

        return df

    except Exception as e:

        st.error(
            f"Erro ao carregar resultados: {e}"
        )

        return pd.DataFrame()