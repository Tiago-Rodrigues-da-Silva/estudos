import streamlit as st
from services.quiz_service import gerar_quiz
from services.resultado_service import salvar

def show_quiz(materia):

    # proteção caso sessão não exista
    if "nome" not in st.session_state or "usuario" not in st.session_state:
        st.error("Usuário não logado")
        st.stop()

    nome = st.session_state.nome
    usuario = st.session_state.usuario

    quiz = gerar_quiz(materia)

    if not quiz:
        st.error("Nenhuma questão encontrada")
        return

    # controla mudança de disciplina
    if "materia" not in st.session_state:
        st.session_state.materia = materia

    if st.session_state.materia != materia:

        # ⭐ NÃO limpar sessão inteira (bug do login)
        st.session_state.materia = materia

        # limpar apenas quiz antigo
        if "quiz" in st.session_state:
            del st.session_state.quiz

        # limpar respostas
        for key in list(st.session_state.keys()):
            if str(key).startswith("q_"):
                del st.session_state[key]

        if "resultado_salvo" in st.session_state:
            del st.session_state.resultado_salvo

    # cria quiz apenas uma vez
    if "quiz" not in st.session_state:
        st.session_state.quiz = quiz

    st.header(materia)

    respondidas = 0
    respostas = []
    total = len(st.session_state.quiz)

    for i, q in enumerate(st.session_state.quiz):

        st.divider()

        # Questão com HTML
        st.markdown(
            f"**Questão {i+1}**: {q['questao']}",
            unsafe_allow_html=True
        )

        escolha = st.radio(
            "Escolha a alternativa:",
            q['opcoes'],
            index=None,
            key=f"q_{i}"
        )

        if escolha is not None:
            respondidas += 1

        respostas.append(escolha)

    # progresso (proteção divisão zero)
    if total > 0:
        st.progress(respondidas / total)

    st.write(f"{respondidas}/{total} respondidas")

    # FINALIZAR
    if st.button("🎯 Finalizar"):

        acertos = 0

        for i, q in enumerate(st.session_state.quiz):

            if respostas[i] is None:
                continue

            if respostas[i] == q['correta']:

                acertos += 1

                st.success(f"Questão {i+1} correta")

            else:

                st.error(f"Questão {i+1} errada")

                st.info(f"Resposta correta: {q['correta']}")

        nota = round(acertos * 0.3, 1)

        nota_formatada = f"{nota:.1f}".replace(".", ",")

        st.metric(
            "🎯 Nota final",
            nota_formatada
        )

        # salvar resultado
        if "resultado_salvo" not in st.session_state:

            salvar(
                usuario,
                nome,
                materia,
                nota
            )

            st.session_state.resultado_salvo = True

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