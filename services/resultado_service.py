import gspread
import pandas as pd
import streamlit as st
import os

from datetime import datetime

from google.oauth2.service_account import Credentials


def conectar():

    scope=[

        "https://www.googleapis.com/auth/spreadsheets",

        "https://www.googleapis.com/auth/drive"

    ]

    # ⭐ local
    if os.path.exists("credentials.json"):

        creds=Credentials.from_service_account_file(

            "credentials.json",

            scopes=scope

        )

    # ⭐ cloud
    else:

        creds=Credentials.from_service_account_info(

            st.secrets["gcp_service_account"]

        ).with_scopes(scope)

    client=gspread.authorize(creds)

    return client


def salvar(nome,materia,nota):

    client=conectar()

    sheet=client.open("resultados_quiz")

    worksheet=sheet.sheet1

    nova_linha=[

        nome,

        materia,

        float(nota),   # ⭐ sempre número real

        datetime.now().strftime("%d/%m/%Y %H:%M")

    ]

    worksheet.append_row(nova_linha)


def carregar_resultados():

    client=conectar()

    sheet=client.open("resultados_quiz")

    worksheet=sheet.sheet1

    dados=worksheet.get_all_records()

    df=pd.DataFrame(dados)

    if df.empty:

        return df

    # ⭐ normalização robusta da nota
    df['Nota']=df['Nota'].astype(str)

    df['Nota']=df['Nota'].str.replace(",",".",regex=False)

    df['Nota']=pd.to_numeric(df['Nota'],errors='coerce')

    # proteção bug 240
    if df['Nota'].max()>10:

        df['Nota']=df['Nota']/100

    return df