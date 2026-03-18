import os
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

def carregar_questoes(nome_planilha):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Caminho absoluto relativo a este arquivo
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # services/
    CRED_PATH = os.path.join(BASE_DIR, "..", "credentials.json")  # sobe para raiz

    if not os.path.exists(CRED_PATH):
        raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {CRED_PATH}")

    creds = Credentials.from_service_account_file(
        CRED_PATH,
        scopes=scope
    )

    client = gspread.authorize(creds)
    sheet = client.open(nome_planilha)
    worksheet = sheet.sheet1
    dados = worksheet.get_all_records()
    df = pd.DataFrame(dados)

    return df