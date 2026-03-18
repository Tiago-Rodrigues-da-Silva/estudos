import pandas as pd

def carregar_csv(path):

    df=pd.read_csv(

        path,
        encoding="utf-8-sig",
        sep=None,
        engine="python"

    )

    df.columns=df.columns.str.strip()

    return df