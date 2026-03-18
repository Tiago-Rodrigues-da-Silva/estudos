import streamlit as st
from services.resultado_service import carregar_resultados
import pandas as pd

def show_home():

    st.title("📊 Resultados do Quiz")

    df = carregar_resultados()

    if df.empty:

        st.info("Nenhum resultado ainda.")
        return

    # ⭐ converter data texto → datetime
    df["Data"] = pd.to_datetime(

        df["Data"],

        format="%d/%m/%Y %H:%M",

        errors="coerce"

    )

    # ⭐ ordenar pela data mais recente primeiro
    df = df.sort_values("Data", ascending=False)

    # dataframe visual
    df_exibir = df.copy()

    # formatar data novamente para padrão brasileiro
    df_exibir["Data"] = df_exibir["Data"].dt.strftime("%d/%m/%Y %H:%M")

    # formatar nota para vírgula
    df_exibir["Nota"] = df_exibir["Nota"].apply(

        lambda x: f"{x:.1f}".replace(".",",")

    )

    st.dataframe(

        df_exibir,

        use_container_width=True,

        hide_index=True

    )