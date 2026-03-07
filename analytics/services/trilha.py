from accounts.models import HabilidadeUsuarioFundamento
from academico.models import DependenciaFundamento


def gerar_trilha_usuario(usuario):

    habilidades = HabilidadeUsuarioFundamento.objects.filter(
        usuario=usuario
    ).select_related("fundamento")

    fracos = [h for h in habilidades if h.habilidade < 600]

    trilha = []

    for h in fracos:

        fundamento = h.fundamento

        prereqs = DependenciaFundamento.objects.filter(
            fundamento=fundamento
        )

        for p in prereqs:

            trilha.append({
                "fundamento": p.prerequisito.nome,
                "motivo": f"Base para {fundamento.nome}"
            })

        trilha.append({
            "fundamento": fundamento.nome,
            "motivo": "Fundamento fraco"
        })

    return trilha