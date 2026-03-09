import re


REGEX_TOPICO = r"^\d+\."
REGEX_SUBTOPICO = r"^[a-z]\."
REGEX_ROMANO = r"^[IVX]+\)"


def detectar_materia(linha):

    linha = linha.strip()

    if not linha.isupper():
        return None

    if len(linha.split()) > 3:
        return None

    if any(x in linha for x in [
        "MINISTÉRIO",
        "COMANDO",
        "DEPARTAMENTO",
        "INSTITUTO",
        "PROGRAMA",
        "VESTIBULAR"
    ]):
        return None

    return linha.title()


def separar_frases(texto):

    partes = re.split(r"\.\s+", texto)

    resultado = []

    for p in partes:

        p = p.strip()

        if not p:
            continue

        resultado.append(p)

    return resultado


def extrair_estrutura(linhas):

    materias = []

    materia_atual = None
    topico_atual = None

    for linha in linhas:

        # ------------------------
        # detectar matéria
        # ------------------------

        materia = detectar_materia(linha)

        if materia:

            materia_atual = {
                "nome": materia,
                "topicos": []
            }

            materias.append(materia_atual)

            topico_atual = None

            continue

        # ------------------------
        # detectar tópico
        # ------------------------

        if re.match(REGEX_TOPICO, linha):

            titulo = re.sub(REGEX_TOPICO, "", linha).strip()

            partes = separar_frases(titulo)

            topico = partes[0]

            fundamentos = partes[1:]

            topico_atual = {
                "titulo": topico,
                "fundamentos": fundamentos
            }

            if materia_atual:
                materia_atual["topicos"].append(topico_atual)

            continue

        # ------------------------
        # subtópicos
        # ------------------------

        if re.match(REGEX_SUBTOPICO, linha) or re.match(REGEX_ROMANO, linha):

            linha = re.sub(REGEX_SUBTOPICO, "", linha)
            linha = re.sub(REGEX_ROMANO, "", linha)

            fundamentos = separar_frases(linha)

            if topico_atual:
                topico_atual["fundamentos"].extend(fundamentos)

            continue

        # ------------------------
        # continuação de tópico
        # ------------------------

        if topico_atual:

            fundamentos = separar_frases(linha)

            topico_atual["fundamentos"].extend(fundamentos)

    return materias