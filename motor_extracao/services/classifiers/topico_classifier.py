TOPICO_KEYWORDS = {

    "Cinemática": [
        "velocidade",
        "aceleração",
        "movimento",
        "mru",
        "mruv"
    ],

    "Dinâmica": [
        "força",
        "segunda lei",
        "newton",
        "massa"
    ],

    "Derivadas": [
        "derivada",
        "taxa de variação",
        "d/dx"
    ],

    "Integrais": [
        "integral",
        "área sob a curva"
    ]
}

from collections import defaultdict


def classificar_topico(texto):

    texto = texto.lower()

    scores = defaultdict(int)

    for topico, palavras in TOPICO_KEYWORDS.items():

        for palavra in palavras:

            if palavra in texto:
                scores[topico] += 1

    if not scores:
        return None

    return max(scores, key=scores.get)