import streamlit as st

from services.quiz_service import gerar_quiz
from services.resultado_service import salvar

nome="Antônia"


def show_quiz(materia):

    quiz=gerar_quiz(materia)

    if len(quiz)==0:

        st.error("Nenhuma questão encontrada")

        return

    # controla mudança de disciplina
    if "materia" not in st.session_state:

        st.session_state.materia=materia

    if st.session_state.materia!=materia:

        st.session_state.clear()

        st.session_state.materia=materia

    # cria quiz apenas uma vez
    if "quiz" not in st.session_state:

        st.session_state.quiz=quiz

    st.header(materia)

    respondidas=0

    respostas=[]

    total=len(st.session_state.quiz)

    for i,q in enumerate(st.session_state.quiz):

        st.divider()

        st.subheader(f"Questão {i+1}")

        st.markdown(f"**Questão {i+1}**: {q['questao']}", unsafe_allow_html=True)
        escolha = st.radio(
            "",
            q['opcoes'],
            index=None,
            key=f"q_{i}"
        )

        if escolha is not None:

            respondidas+=1

        respostas.append(escolha)

    st.progress(respondidas/total)

    st.write(f"{respondidas}/{total}")

    # FINALIZAR
    if st.button("🎯 Finalizar"):

        acertos=0

        for i,q in enumerate(st.session_state.quiz):

            if respostas[i] is None:

                continue

            if respostas[i]==q['correta']:

                acertos+=1

                st.success(f"Questão {i+1} correta")

            else:

                st.error(f"Questão {i+1} errada")

                st.info(f"Resposta correta: {q['correta']}")

        nota=round(acertos*0.3,1)

        # ⭐ formatação brasileira apenas visual
        nota_formatada=f"{nota:.1f}".replace(".",",")

        st.metric(

            "🎯 Nota final",

            nota_formatada

        )

        # salva só uma vez
        if "resultado_salvo" not in st.session_state:

            salvar(

                nome,
                materia,
                nota   # ⭐ salva como número

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