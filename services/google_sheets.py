import gspread
import pandas as pd

from google.oauth2.service_account import Credentials


def carregar_questoes(nome_planilha):

    scope=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds=Credentials.from_service_account_file(

        "credentials.json",
        scopes=scope

    )

    client=gspread.authorize(creds)

    sheet=client.open(nome_planilha)

    worksheet=sheet.sheet1

    dados=worksheet.get_all_records()

    df=pd.DataFrame(dados)

    return df