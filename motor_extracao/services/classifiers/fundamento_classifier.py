from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from academico.models import Fundamento

model = SentenceTransformer("all-MiniLM-L6-v2")


def classificar_fundamentos(texto, top_k=3):

    fundamentos = Fundamento.objects.select_related(
        "topico",
        "topico__materia"
    )

    docs = []

    for f in fundamentos:

        docs.append(
            f"{f.nome}. "
            f"Tópico: {f.topico.nome}. "
            f"Matéria: {f.topico.materia.nome}. "
            f"{f.descricao}"
        )

    emb_docs = model.encode(docs)

    emb_questao = model.encode([texto])

    scores = cosine_similarity(emb_questao, emb_docs)[0]

    ranking = list(zip(fundamentos, scores))

    ranking.sort(key=lambda x: x[1], reverse=True)

    return [f for f, score in ranking[:top_k]]