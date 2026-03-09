from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from academico.models import Topico

model = SentenceTransformer("all-MiniLM-L6-v2")


def classificar_topico_semantico(texto):

    topicos = Topico.objects.all()

    textos_topicos = []

    for t in topicos:
        textos_topicos.append(f"{t.nome} {t.descricao}")

    emb_topicos = model.encode(textos_topicos)

    emb_questao = model.encode([texto])

    scores = cosine_similarity(emb_questao, emb_topicos)[0]

    indice = scores.argmax()

    return topicos[indice]