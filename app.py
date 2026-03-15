import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(

    page_title="Quiz Kids",
    page_icon="⭐",
    layout="wide"

)

# CSS mobile + scroll top
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

div[data-baseweb="radio"]{

font-size:18px;

}

/* scroll topo */

html {
scroll-behavior:smooth;
}

</style>

""", unsafe_allow_html=True)

nome="Antônia"

st.title("⭐ Plataforma de Estudos")

# MENU
st.sidebar.title("Matérias")

materia = st.sidebar.radio(

"Escolha a matéria:",

[
"Português",
"Matemática",
"Geografia",
"História"
]

)

arquivo = materia.replace("ê","e").replace("á","a").replace("í","i")+".csv"

st.sidebar.success(materia)

# carregar CSV
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

# limpar colunas
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

    st.write(df.columns.tolist())

    st.stop()

df=df.dropna()

df=df.reset_index(drop=True)

# reset se trocar matéria
if "materia" not in st.session_state:

    st.session_state.materia=materia

if st.session_state.materia!=materia:

    st.session_state.clear()

    st.session_state.materia=materia

# gerar quiz
if "quiz" not in st.session_state:

    df=df.drop_duplicates(subset=['Questão'])

    quiz_df=df.sample(min(10,len(df))).reset_index(drop=True)

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

# topo (ancora)
st.markdown("<div id='top'></div>",unsafe_allow_html=True)

st.header(f"📚 {materia}")

respondidas=0

respostas=[]

total=len(st.session_state.quiz)

for i,q in enumerate(st.session_state.quiz):

    st.divider()

    st.subheader(f"Questão {i+1}")

    letras=["A","B","C"]

    opcoes_formatadas=["-- Escolha --"]

    for j,op in enumerate(q['opcoes']):

        opcoes_formatadas.append(f"{letras[j]}) {op}")

    escolha=st.radio(

        q['questao'],

        opcoes_formatadas,

        index=0,

        key=f"q_{i}"

    )

    if escolha!="-- Escolha --":

        respondidas+=1

    respostas.append(escolha)

# progresso
st.progress(respondidas/total)

st.write(f"{respondidas}/{total} respondidas")

# FINALIZAR
if st.button("🎯 Finalizar"):

    acertos=0

    st.divider()

    st.header("Resultado")

    for i,q in enumerate(st.session_state.quiz):

        if respostas[i].endswith(q['correta']):

            acertos+=1

            st.success(f"Questão {i+1} correta")

        else:

            st.error(f"Questão {i+1} errada")

            st.info(f"Resposta correta: {q['correta']}")

    st.metric("Acertos",f"{acertos}/{total}")

    if acertos>=9:

        estrelas=3

    elif acertos>=7:

        estrelas=2

    elif acertos>=5:

        estrelas=1

    else:

        estrelas=0

    estrelas_txt="⭐"*estrelas

    if estrelas==0:

        estrelas_txt="😢"

    st.header(estrelas_txt)

    if estrelas==3:

        st.balloons()

        st.success(f"Excelente {nome}! 🏆")

    elif estrelas==2:

        st.success(f"Muito bem {nome}! 👏")

    elif estrelas==1:

        st.info(f"Bom trabalho {nome}! 📚")

    else:

        st.warning(f"{nome}, vamos treinar mais! 💪")

# NOVO JOGO UX PERFEITA
if st.button("🔄 Novo jogo"):

    # limpar quiz
    if "quiz" in st.session_state:

        del st.session_state["quiz"]

    # limpar respostas
    for key in list(st.session_state.keys()):

        if str(key).startswith("q_"):

            del st.session_state[key]

    # voltar topo
    st.markdown("""

    <script>

    window.scrollTo(0,0);

    </script>

    """,unsafe_allow_html=True)

    st.rerun()