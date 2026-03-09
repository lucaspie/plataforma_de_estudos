from sentence_transformers import SentenceTransformer
from academico.models import FundamentoEmbedding

model = SentenceTransformer("all-MiniLM-L6-v2")


def gerar_embedding(texto):
    return model.encode(texto)

def gerar_embedding_fundamento(fundamento):

    vetor = gerar_embedding(fundamento.nome).tolist()

    FundamentoEmbedding.objects.update_or_create(
        fundamento=fundamento,
        defaults={"vetor": vetor}
    )