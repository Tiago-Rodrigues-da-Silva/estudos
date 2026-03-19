import random
from services.google_sheets import carregar_questoes

def gerar_quiz(materia):
    sheets = {
        "Matemática": "questoes_matematica",
        "Português": "questoes_portugues",
        "Geografia": "questoes_geografia",
        "História": "questoes_historia",
        "Espanhol": "questoes_espanhol"
    }

    nome_sheet = sheets.get(materia)
    if not nome_sheet:
        return []

    df = carregar_questoes(nome_sheet)
    if df.empty:
        return []

    # padronizar nomes
    df.columns = df.columns.str.strip().str.lower()

    colunas = ["id", "questao", "a", "b", "c", "correta"]
    if not all(col in df.columns for col in colunas):
        return []

    df = df.dropna()
    df = df.drop_duplicates(subset=['questao'])

    # sortear até 10 questões
    quiz_df = df.sample(min(10, len(df)))

    perguntas = []
    for _, row in quiz_df.iterrows():
        alternativas = {
            "A": row['a'],
            "B": row['b'],
            "C": row['c']
        }

        opcoes = list(alternativas.values())
        random.shuffle(opcoes)

        # pegar a resposta correta
        correta = alternativas[row['correta']]

        # mantém HTML na questão
        questao_html = row['questao']

        perguntas.append({
            "id": row['id'],
            "questao": questao_html,  # aqui o HTML é preservado
            "correta": correta,
            "opcoes": opcoes
        })

    return perguntas