import re

ALT_REGEX = r"\s([A-E])\)"


def extrair_alternativas(conteudo):

    partes = re.split(ALT_REGEX, conteudo)

    if len(partes) < 3:
        return None

    enunciado = partes[0]

    alternativas = {}

    for i in range(1, len(partes), 2):

        letra = partes[i]
        texto = partes[i+1]

        alternativas[letra] = texto.strip()

    return enunciado, alternativas