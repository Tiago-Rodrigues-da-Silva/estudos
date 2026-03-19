from services.google_sheets import carregar_questoes

def autenticar(usuario, senha):

    df = carregar_questoes("usuarios")

    if df.empty:
        return None

    # padronizar colunas
    df.columns = df.columns.str.strip().str.lower()

    # força tudo como texto (corrige zero à esquerda)
    df["usuario"] = df["usuario"].astype(str).str.strip()
    df["senha"] = df["senha"].astype(str).str.strip()

    usuario = str(usuario).strip()
    senha = str(senha).strip()

    user = df[
        (df["usuario"] == usuario) &
        (df["senha"] == senha)
    ]

    if user.empty:
        return None

    return user.iloc[0]["nome"]