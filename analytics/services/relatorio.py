from collections import defaultdict
from django.db.models import Avg
from avaliacao.models import HistoricoResolucao
from academico.models import DependenciaFundamento


def relatorio_materia(usuario, materia):

    historico = HistoricoResolucao.objects.filter(
        usuario=usuario,
        questao__topico__materia=materia
    ).select_related(
        "questao__topico__materia"
    ).prefetch_related(
        "questao__fundamentos",
        "questao__fundamentos__dependencias__prerequisito"
    )

    total = historico.count()
    acertos = historico.filter(acertou=True).count()

    taxa_acerto = round((acertos / total) * 100) if total else 0

    tempo_medio = historico.aggregate(
        Avg("tempo_em_segundos")
    )["tempo_em_segundos__avg"] or 0

    stats = defaultdict(lambda: {
        "fundamento": "",
        "acertos": 0,
        "total": 0,
        "obj": None
    })

    for r in historico:

        for f in r.questao.fundamentos.all():

            chave = f.id

            stats[chave]["fundamento"] = f.nome
            stats[chave]["obj"] = f
            stats[chave]["total"] += 1

            if r.acertou:
                stats[chave]["acertos"] += 1

    fundamentos = []
    nodes = []
    edges = []

    for fid, s in stats.items():

        taxa = s["acertos"] / s["total"] if s["total"] else 0
        rating = int(300 + taxa * 700)

        fundamentos.append({
            "fundamento": s["fundamento"],
            "taxa": int(taxa * 100),
            "rating": rating
        })

        nodes.append({
            "data": {
                "id": str(fid),
                "label": s["fundamento"],
                "rating": rating,
                "taxa": int(taxa * 100)
            }
        })

        fundamento_obj = s["obj"]

        for dep in fundamento_obj.dependencias.all():

            prereq = dep.prerequisito

            if prereq.id in stats:

                edges.append({
                    "data": {
                        "source": str(prereq.id),
                        "target": str(fid),
                        "peso": dep.peso
                    }
                })

    fundamentos.sort(key=lambda x: x["rating"])

    return {
        "taxa_acerto": taxa_acerto,
        "total_respondidas": total,
        "tempo_medio": round(tempo_medio, 1),
        "fundamentos": fundamentos,
        "mapa": {
            "nodes": nodes,
            "edges": edges
        }
    }