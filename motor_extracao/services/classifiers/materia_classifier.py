MATERIA_KEYWORDS = {

    "Matemática": [
        "derivada",
        "integral",
        "limite",
        "matriz",
        "determinante",
        "log",
        "sen",
        "cos",
        "tan",
        "polinômio",
        "progressão",
        "combinatória",
        "probabilidade"
    ],

    "Física": [
        "velocidade",
        "aceleração",
        "força",
        "energia",
        "trabalho",
        "campo elétrico",
        "corrente",
        "tensão",
        "resistência",
        "massa",
        "movimento"
    ],

    "Química": [
        "mol",
        "reação",
        "equilíbrio",
        "pH",
        "ácido",
        "base",
        "ligação",
        "orgânico",
        "estequiometria"
    ]
}

from collections import defaultdict


def classificar_materia(texto):

    texto = texto.lower()

    scores = defaultdict(int)

    for materia, palavras in MATERIA_KEYWORDS.items():

        for palavra in palavras:

            if palavra in texto:
                scores[materia] += 1

    if not scores:
        return None

    return max(scores, key=scores.get)