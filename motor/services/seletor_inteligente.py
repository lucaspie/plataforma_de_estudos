import random

from academico.models import Questao
from accounts.models import HabilidadeUsuarioFundamento
from avaliacao.models import HistoricoResolucao
from motor.services.nivelamento import probabilidade_acerto


def selecionar_questoes_adaptativas(
    usuario,
    queryset_base,
    quantidade=20
):

    questoes = list(queryset_base.prefetch_related("fundamentos", "opcoes"))

    if not questoes:
        return []

    # histórico do usuário
    historico = HistoricoResolucao.objects.filter(usuario=usuario)

    resolvidas = set(
        historico.values_list("questao_id", flat=True)
    )

    # habilidades do usuário
    habilidades = {
        h.fundamento_id: h.habilidade
        for h in HabilidadeUsuarioFundamento.objects.filter(usuario=usuario)
    }

    candidatos = []

    for q in questoes:

        fundamentos = q.fundamentos.all()

        if not fundamentos:
            continue

        # habilidade média do aluno nesses fundamentos
        H = sum(
            habilidades.get(f.id, 0)
            for f in fundamentos
        ) / len(fundamentos)

        D = q.nivel_dinamico

        P = probabilidade_acerto(H, D)

        # score ideal próximo de 70%
        score = 1 - abs(P - 0.7)

        # penalizar questões já resolvidas
        if q.id in resolvidas:
            score *= 0.5

        candidatos.append((q, score))

    # ordenar pelo score
    candidatos.sort(key=lambda x: x[1], reverse=True)

    selecionadas = [q for q, _ in candidatos[:quantidade]]

    return selecionadas