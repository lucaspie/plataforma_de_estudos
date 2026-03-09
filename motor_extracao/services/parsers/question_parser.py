import re

QUESTAO_REGEX = r"\n\s*(\d{1,3})\."


def extrair_questoes(texto):

    partes = re.split(QUESTAO_REGEX, texto)

    questoes = []

    for i in range(1, len(partes), 2):

        numero = int(partes[i])
        conteudo = partes[i+1]

        questoes.append({
            "numero": numero,
            "conteudo": conteudo
        })

    return questoes