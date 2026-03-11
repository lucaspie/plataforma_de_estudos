from sentence_transformers import SentenceTransformer
from academico.models import FundamentoEmbedding

model = SentenceTransformer("all-MiniLM-L6-v2")


def gerar_embedding(dados):

    textos = [d["nome"] for d in dados]

    embeddings = model.encode(textos)

    for i, emb in enumerate(embeddings):
        dados[i]["embedding"] = emb

    return dados


def gerar_embedding_texto(texto):
    return model.encode(texto)


def gerar_embedding_fundamento(fundamento):

    vetor = gerar_embedding_texto(fundamento.nome).tolist()

    FundamentoEmbedding.objects.update_or_create(
        fundamento=fundamento,
        defaults={"vetor": vetor}
    )