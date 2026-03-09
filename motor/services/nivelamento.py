import math
from django.db import transaction

from accounts.models import HabilidadeUsuarioFundamento
from academico.models import Questao

K_ALUNO = 32
K_QUESTAO = 12


def probabilidade_acerto(rating_aluno, rating_questao):
    return 1 / (1 + 10 ** ((rating_questao - rating_aluno) / 400))


@transaction.atomic
def atualizar_rating(usuario, questao, acertou):

    fundamentos = list(questao.fundamentos.all())

    habilidades = []

    objetos_habilidade = []

    for fundamento in fundamentos:

        habilidade_obj, _ = HabilidadeUsuarioFundamento.objects.get_or_create(
            usuario=usuario,
            fundamento=fundamento,
            defaults={"habilidade": 0}
        )

        objetos_habilidade.append(habilidade_obj)
        habilidades.append(habilidade_obj.habilidade)

    if not habilidades:
        return

    rating_aluno = sum(habilidades) / len(habilidades)
    rating_questao = questao.nivel_dinamico

    P = probabilidade_acerto(rating_aluno, rating_questao)
    resultado = 1 if acertou else 0

    # Atualiza aluno
    for habilidade_obj in objetos_habilidade:

        habilidade_obj.habilidade += K_ALUNO * (resultado - P)
        habilidade_obj.save()

    # Atualiza questão (UMA vez)
    questao.nivel_dinamico += K_QUESTAO * (P - resultado)

    questao.total_respostas += 1

    if acertou:
        questao.total_acertos += 1

    questao.save()