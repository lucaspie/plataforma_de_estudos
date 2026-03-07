from accounts.models import HabilidadeUsuarioFundamento
from .skill_graph import obter_prerequisitos
from motor.services.learning_engine import detectar_fraquezas

def diagnostico_usuario(usuario):

    habilidades = HabilidadeUsuarioFundamento.objects.filter(
        usuario=usuario
    ).select_related(
        "fundamento",
        "fundamento__topico",
        "fundamento__topico__materia"
    )

    fortes = []
    fracos = []

    for h in habilidades:

        item = {
            "fundamento": h.fundamento.nome,
            "topico": h.fundamento.topico.nome,
            "materia": h.fundamento.topico.materia.nome,
            "rating": h.habilidade
        }

        if h.habilidade > 200:
            fortes.append(item)

        if h.habilidade < -200:
            fracos.append(item)

    fortes.sort(key=lambda x: x["rating"], reverse=True)
    fracos.sort(key=lambda x: x["rating"])

    return {
        "fortes": fortes[:10],
        "fracos": fracos[:10]
    }

def diagnostico_profundidade(usuario):

    fracos, medios, fortes = detectar_fraquezas(usuario)

    causas = {}

    for f in fracos:

        prereqs = obter_prerequisitos(f)

        causas[f] = [p.nome for p in prereqs]

    return causas