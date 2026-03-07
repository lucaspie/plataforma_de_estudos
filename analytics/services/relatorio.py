from collections import defaultdict
from avaliacao.models import HistoricoResolucao

def relatorio_materia(usuario, materia):


    historico = HistoricoResolucao.objects.filter(
        usuario=usuario,
        questao__topico__materia=materia
    ).select_related(
        "questao__topico__materia"
    ).prefetch_related(
        "questao__fundamentos"
    )

    stats = defaultdict(lambda:{
        "fundamento":"",
        "acertos":0,
        "total":0
    })

    for r in historico:
        for f in r.questao.fundamentos.all():

            chave = f.id

            stats[chave]["fundamento"] = f.nome
            stats[chave]["total"] += 1

            if r.acertou:
                stats[chave]["acertos"] += 1

    resultados = []

    for s in stats.values():

        taxa = s["acertos"] / s["total"] if s["total"] else 0
        rating = int(300 + taxa * 700)

        resultados.append({
            "fundamento": s["fundamento"],
            "taxa": int(taxa*100),
            "rating": rating
        })

    resultados.sort(key=lambda x:x["rating"])

    return resultados