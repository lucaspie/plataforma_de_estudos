import re

GABARITO_REGEX = r"(\d+)\s*[-–]\s*([A-E])"


def extrair_gabarito(texto):

    respostas = {}

    for numero, letra in re.findall(GABARITO_REGEX, texto):

        respostas[int(numero)] = letra

    return respostas