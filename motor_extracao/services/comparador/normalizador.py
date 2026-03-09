import re
import unicodedata
from rapidfuzz import fuzz


def normalizar_texto(texto):

    texto = texto.lower()

    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")

    texto = re.sub(r"[^\w\s]", "", texto)

    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()

def similares(a, b, limite=90):

    a = normalizar_texto(a)
    b = normalizar_texto(b)

    score = fuzz.token_set_ratio(a, b)

    return score >= limite

def encontrar_similar(nome, queryset):

    for obj in queryset:

        if similares(nome, obj.nome):

            return obj

    return None

def encontrar_materia_existente(nome, materias_db):

    for m in materias_db:

        if similares(nome, m.nome):
            return m

    return None