from motor_extracao.services.semantica.clusterizador import clusterizar_fundamentos
from motor_extracao.services.semantica.embeddings import gerar_embedding


def test_clusterizador_puro():

    dados = [
        {"nome": "Velocidade média"},
        {"nome": "Velocidade escalar média"},
        {"nome": "Cálculo da velocidade média"},
        {"nome": "Aceleração"},
    ]

    dados = gerar_embedding(dados)

    class F:
        def __init__(self, nome, embedding):
            self.nome = nome
            self.embedding = embedding

    objs = [F(d["nome"], d["embedding"]) for d in dados]

    clusters = clusterizar_fundamentos(objs)
    print(len(clusters))

    # deve existir pelo menos um cluster
    assert len(clusters) >= 1