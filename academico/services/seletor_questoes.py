import random

from django.db.models import Q

from academico.models import Questao
from avaliacao.models import HistoricoResolucao


def selecionar_questoes(
    usuario,
    queryset_base,
    quantidade=20,
    incluir_erradas=True,
    evitar_repetidas=True
):
    """
    Motor de seleção inteligente de questões
    """

    questoes = list(queryset_base.prefetch_related("opcoes"))

    if not questoes:
        return []

    # histórico do usuário
    historico = HistoricoResolucao.objects.filter(
        usuario=usuario
    )

    questoes_erradas = set(
        historico.filter(acertou=False).values_list("questao_id", flat=True)
    )

    questoes_acertadas = set(
        historico.filter(acertou=True).values_list("questao_id", flat=True)
    )

    selecionadas = []

    # 1️⃣ priorizar questões erradas
    if incluir_erradas:

        erradas = [q for q in questoes if q.id in questoes_erradas]

        random.shuffle(erradas)

        selecionadas.extend(erradas[: quantidade // 3])

    # 2️⃣ novas questões (nunca resolvidas)
    novas = [
        q for q in questoes
        if q.id not in questoes_erradas
        and q.id not in questoes_acertadas
    ]

    random.shuffle(novas)

    selecionadas.extend(novas[: quantidade])

    # 3️⃣ evitar repetidas acertadas
    if evitar_repetidas:

        selecionadas = [
            q for q in selecionadas
            if q.id not in questoes_acertadas
        ]

    # completar se faltar
    if len(selecionadas) < quantidade:

        restantes = [q for q in questoes if q not in selecionadas]

        random.shuffle(restantes)

        selecionadas.extend(restantes[: quantidade - len(selecionadas)])

    return selecionadas[:quantidade]