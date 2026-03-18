import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime

st.set_page_config(

    page_title="Quiz Kids",
    page_icon="⭐",
    layout="wide"

)

# CSS
st.markdown("""

<style>

.stButton button {

width:100%;
height:55px;
font-size:18px;
border-radius:12px;
background-color:#4CAF50;
color:white;

}

</style>

""", unsafe_allow_html=True)

nome="Antônia"

# salvar resultado
def salvar_resultado(nome,materia,acertos,total):

    arquivo="resultados.csv"

    nota=round(acertos*0.3,1)

    novo=pd.DataFrame([{

        "Nome":nome,
        "Disciplina":materia,
        "Nota":nota,
        "Data":datetime.now().strftime("%Y-%m-%d %H:%M")

    }])

    if os.path.exists(arquivo):

        antigo=pd.read_csv(arquivo)

        antigo.columns=antigo.columns.str.strip()

        # compatibilidade
        antigo=antigo.rename(columns={

            "nome":"Nome",
            "disciplina":"Disciplina",
            "acertos":"Acertos",
            "total":"Total",
            "data_hora":"Data"

        })

        if "Nota" not in antigo.columns:

            if "Acertos" in antigo.columns:

                antigo["Nota"]=round(antigo["Acertos"]*0.3,1)

        if "Data" not in antigo.columns:

            antigo["Data"]=""

        antigo=antigo[["Nome","Disciplina","Nota","Data"]]

        df=pd.concat([antigo,novo],ignore_index=True)

    else:

        df=novo

    df.to_csv(arquivo,index=False)

# MENU
st.sidebar.title("Menu")

pagina=st.sidebar.radio(

"Escolha:",

[

"🏠 Home",
"Português",
"Matemática",
"Geografia",
"História"

]

)

# HOME
if pagina=="🏠 Home":

    st.title("⭐ Plataforma de Estudos")

    st.header("Histórico de Resultados")

    if os.path.exists("resultados.csv"):

        df=pd.read_csv("resultados.csv")

        df.columns=df.columns.str.strip()

        df=df.rename(columns={

            "nome":"Nome",
            "disciplina":"Disciplina",
            "data_hora":"Data"

        })

        if "Nota" not in df.columns:

            if "Acertos" in df.columns:

                df["Nota"]=round(df["Acertos"]*0.3,1)

            elif "acertos" in df.columns:

                df["Nota"]=round(df["acertos"]*0.3,1)

        if "Data" not in df.columns:

            df["Data"]=""

        df=df[["Nome","Disciplina","Nota","Data"]]

        df=df.sort_values("Data",ascending=False)

        st.dataframe(

            df,

            use_container_width=True

        )

        st.metric(

            "Total de tentativas",

            len(df)

        )

    else:

        st.info("Nenhum resultado ainda")

    st.stop()

# QUIZ
materia=pagina

arquivo=materia.replace("ê","e").replace("á","a").replace("í","i")+".csv"

if os.path.exists(arquivo):

    df=pd.read_csv(

        arquivo,
        encoding="utf-8-sig",
        sep=None,
        engine="python",
        on_bad_lines="skip"

    )

else:

    st.error("Arquivo não encontrado")

    st.stop()

df.columns=(

    df.columns
    .str.strip()
    .str.replace('\ufeff','')

)

colunas=[

"Questão",
"Correta",
"Incorreta1",
"Incorreta2"

]

if not all(col in df.columns for col in colunas):

    st.error("CSV inválido")

    st.stop()

df=df.dropna()

df=df.reset_index(drop=True)

# reset matéria
if "materia" not in st.session_state:

    st.session_state.materia=materia

if st.session_state.materia!=materia:

    st.session_state.clear()

    st.session_state.materia=materia

# gerar quiz
if "quiz" not in st.session_state:

    df=df.drop_duplicates(subset=['Questão'])

    quiz_df=df.sample(min(10,len(df)))

    perguntas=[]

    for _,row in quiz_df.iterrows():

        opcoes=[

            row['Correta'],
            row['Incorreta1'],
            row['Incorreta2']

        ]

        random.shuffle(opcoes)

        perguntas.append({

            "questao":row['Questão'],
            "correta":row['Correta'],
            "opcoes":opcoes

        })

    st.session_state.quiz=perguntas

st.header(materia)

respondidas=0

respostas=[]

total=len(st.session_state.quiz)

for i,q in enumerate(st.session_state.quiz):

    st.divider()

    st.subheader(f"Questão {i+1}")

    opcoes=["-- Escolha --"]

    letras=["A","B","C"]

    for j,op in enumerate(q['opcoes']):

        opcoes.append(f"{letras[j]}) {op}")

    escolha=st.radio(

        q['questao'],
        opcoes,
        index=0,
        key=f"q_{i}"

    )

    if escolha!="-- Escolha --":

        respondidas+=1

    respostas.append(escolha)

st.progress(respondidas/total)

st.write(f"{respondidas}/{total}")

# FINALIZAR
if st.button("🎯 Finalizar"):

    acertos=0

    for i,q in enumerate(st.session_state.quiz):

        if respostas[i].endswith(q['correta']):

            acertos+=1

            st.success(f"Questão {i+1} correta")

        else:

            st.error(f"Questão {i+1} errada")

            st.info(f"Resposta correta: {q['correta']}")

    nota=round(acertos*0.3,1)

    st.metric("Nota",nota)

    if "resultado_salvo" not in st.session_state:

        salvar_resultado(

            nome,
            materia,
            acertos,
            total

        )

        st.session_state.resultado_salvo=True

# NOVO JOGO
if st.button("🔄 Novo jogo"):

    if "quiz" in st.session_state:

        del st.session_state["quiz"]

    for key in list(st.session_state.keys()):

        if str(key).startswith("q_"):

            del st.session_state[key]

    if "resultado_salvo" in st.session_state:

        del st.session_state["resultado_salvo"]

    st.rerun()