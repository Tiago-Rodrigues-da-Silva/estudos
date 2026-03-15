import streamlit as st
import pandas as pd
import random
import os

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

div[data-baseweb="radio"]{
font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# nome fixo
nome="Antônia"

st.title("⭐ Plataforma de Estudos")

# MENU LATERAL
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

arquivo = materia.replace("ê","e").replace("á","a").replace("ó","o")+".csv"

st.sidebar.write(f"Matéria atual:")
st.sidebar.success(materia)

# carregar CSV
if os.path.exists(arquivo):

    df=pd.read_csv(arquivo,encoding="utf-8")

    df.columns=['questao','correta']

else:

    st.error("Arquivo não encontrado")
    st.stop()

# reiniciar quiz quando trocar matéria
if "materia" not in st.session_state:

    st.session_state.materia=materia

if st.session_state.materia!=materia:

    st.session_state.clear()
    st.session_state.materia=materia

# gerar quiz
if "quiz" not in st.session_state:

    quiz_df=df.sample(min(10,len(df)))

    perguntas=[]

    todas=df['correta'].tolist()

    for _,row in quiz_df.iterrows():

        correta=row['correta']

        erradas=[]

        while len(erradas)<2:

            r=random.choice(todas)

            if r!=correta and r not in erradas:

                erradas.append(r)

        opcoes=[correta]+erradas

        random.shuffle(opcoes)

        perguntas.append({

            "questao":row['questao'],

            "correta":correta,

            "opcoes":opcoes

        })

    st.session_state.quiz=perguntas

# titulo matéria
st.header(f"📚 {materia}")

respondidas=0

respostas=[]

for i,q in enumerate(st.session_state.quiz):

    st.divider()

    st.subheader(f"Questão {i+1}")

    opcoes=["-- Escolha --"]+q['opcoes']

    escolha=st.radio(

        q['questao'],

        opcoes,

        index=0,

        key=i

    )

    if escolha!="-- Escolha --":

        respondidas+=1

    respostas.append(escolha)

# progresso
st.progress(respondidas/10)

st.write(f"{respondidas}/10 respondidas")

# finalizar
if st.button("🎯 Finalizar"):

    acertos=0

    for i,q in enumerate(st.session_state.quiz):

        if respostas[i]==q['correta']:

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