MATERIAS_VALIDAS = {
    "FÍSICA",
    "MATEMÁTICA",
    "QUÍMICA",
    "PORTUGUÊS",
    "INGLÊS",
    "REDAÇÃO",
}

def detectar_materias(linhas):

    materias = []
    atual = None

    for linha in linhas:

        linha = linha.strip()

        if not linha:
            continue

        linha_upper = linha.upper()

        if linha_upper in MATERIAS_VALIDAS:

            atual = {
                "nome": linha_upper.title(),
                "linhas": []
            }

            materias.append(atual)

            continue

        if atual:
            atual["linhas"].append(linha)

    return materias