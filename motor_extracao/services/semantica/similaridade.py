import numpy as np
from .embeddings import gerar_embedding
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def similaridade_semantica(a, b):

    emb_a = gerar_embedding(a)
    emb_b = gerar_embedding(b)

    score = cosine_similarity(
        [emb_a],
        [emb_b]
    )[0][0]

    return float(score)