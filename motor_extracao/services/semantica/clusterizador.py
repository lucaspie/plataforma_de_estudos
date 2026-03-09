from sklearn.cluster import DBSCAN
import numpy as np


def clusterizar_fundamentos(fundamentos):

    embeddings = np.array([f.embedding for f in fundamentos])

    modelo = DBSCAN(
        eps=0.3,
        min_samples=2,
        metric="cosine"
    )

    labels = modelo.fit_predict(embeddings)

    clusters = {}

    for f, label in zip(fundamentos, labels):

        if label == -1:
            continue

        clusters.setdefault(label, []).append(f)

    return clusters