from celery import shared_task

from django.contrib.auth import get_user_model

from academico.models import Questao
from motor.services.nivelamento import atualizar_rating

User = get_user_model()

@shared_task
def processar_resposta(usuario_id, questao_id, acertou):
    usuario = User.objects.get(id=usuario_id)
    questao = Questao.objects.get(id=questao_id)

    atualizar_rating(usuario, questao, acertou)

    #Na view onde criar HistoricoResolucao:
    #processar_resposta.delay(usuario.id, questao.id, acertou)