import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(

    page_title="Quiz Kids",

    page_icon="⭐",

    layout="wide"

)

# CSS mobile
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

</style>

""", unsafe_allow_html=True)

# nome fixo
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

# nome arquivo
arquivo = materia.replace("ê","e").replace("á","a").replace("í","i")+".csv"

st.sidebar.success(materia)

# carregar CSV
if os.path.exists(arquivo):

    df=pd.read_csv(
        arquivo,
        encoding="utf-8",
        sep=None,
        engine="python",
        on_bad_lines="skip"
        )

else:

    st.error("Arquivo não encontrado")

    st.stop()

# reiniciar se trocar matéria
if "materia" not in st.session_state:

    st.session_state.materia=materia

if st.session_state.materia!=materia:

    st.session_state.clear()

    st.session_state.materia=materia

# gerar quiz
if "quiz" not in st.session_state:

    # remover duplicadas
    df=df.drop_duplicates(subset=['Questão'])

    # selecionar 10 aleatórias
    quiz_df=df.sample(min(10,len(df))).reset_index(drop=True)

    perguntas=[]

    for _,row in quiz_df.iterrows():

        opcoes=[

            row['Resposta Correta'],

            row['Incorreta 1'],

            row['Incorreta 2']

        ]

        random.shuffle(opcoes)

        perguntas.append({

            "questao":row['Questão'],

            "correta":row['Resposta Correta'],

            "opcoes":opcoes

        })

    st.session_state.quiz=perguntas

# titulo
st.header(f"📚 {materia}")

respondidas=0

respostas=[]

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

        key=i

    )

    if escolha!="-- Escolha --":

        respondidas+=1

    respostas.append(escolha)

# progresso
st.progress(respondidas/10)

st.write(f"{respondidas}/10 respondidas")

# FINALIZAR
if st.button("🎯 Finalizar"):

    acertos=0

    for i,q in enumerate(st.session_state.quiz):

        if q['correta'] in respostas[i]:

            acertos+=1

    st.divider()

    st.header("Resultado")

    st.metric("Acertos",f"{acertos}/10")

# estrelas

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

# mensagens

    if estrelas==3:

        st.balloons()

        st.success(f"Excelente {nome}! 🏆")

    elif estrelas==2:

        st.success(f"Muito bem {nome}! 👏")

    elif estrelas==1:

        st.info(f"Bom trabalho {nome}! 📚")

    else:

        st.warning(f"{nome}, vamos treinar mais! 💪")

# novo jogo
if st.button("🔄 Novo jogo"):

    st.session_state.quiz=None

    st.rerun()