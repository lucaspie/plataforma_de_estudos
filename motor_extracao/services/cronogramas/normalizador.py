import re

def normalizar_linhas(texto):

    linhas = texto.split("\n")

    resultado = []
    buffer = ""

    for linha in linhas:

        linha = linha.strip()

        if not linha:
            continue

        # remover números de página
        if re.match(r"^\d+$", linha):
            continue

        # se for matéria (caixa alta)
        if linha.isupper():

            if buffer:
                resultado.append(buffer.strip())
                buffer = ""

            resultado.append(linha)
            continue

        # se for tópico numerado
        if re.match(r"^\d+\.", linha):

            if buffer:
                resultado.append(buffer.strip())
                buffer = ""

            resultado.append(linha)
            continue

        # se linha anterior terminou com palavra cortada
        if buffer and not buffer.endswith((".", ":", ";")):
            buffer += " " + linha
        else:
            if buffer:
                resultado.append(buffer.strip())
            buffer = linha

    if buffer:
        resultado.append(buffer.strip())

    return resultado