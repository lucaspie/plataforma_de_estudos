import math
from django.db import transaction

from accounts.models import HabilidadeUsuarioFundamento
from academico.models import Questao

K_ALUNO = 24
K_QUESTAO = 8


def probabilidade_acerto(rating_aluno, rating_questao):
    return 1 / (1 + 10 ** ((rating_questao - rating_aluno) / 400))


@transaction.atomic
def atualizar_rating(usuario, questao, acertou):

    fundamentos = questao.fundamentos.all()

    for fundamento in fundamentos:

        habilidade_obj, _ = HabilidadeUsuarioFundamento.objects.get_or_create(
            usuario=usuario,
            fundamento=fundamento,
            defaults={"habilidade": 0}
        )

        rating_aluno = habilidade_obj.habilidade
        rating_questao = questao.nivel_dinamico

        P = probabilidade_acerto(rating_aluno, rating_questao)
        resultado = 1 if acertou else 0

        # Atualiza aluno
        rating_aluno_novo = rating_aluno + K_ALUNO * (resultado - P)
        habilidade_obj.habilidade = rating_aluno_novo
        habilidade_obj.save()

        # Atualiza questão
        rating_questao_novo = rating_questao + K_QUESTAO * (P - resultado)
        questao.nivel_dinamico = rating_questao_novo

    questao.total_respostas += 1
    if acertou:
        questao.total_acertos += 1

    questao.save()