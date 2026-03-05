from django.db import models
from django.conf import settings

from academico.models import Questao, Opcao, Concurso

class HistoricoResolucao(models.Model):

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="historico"
    )

    questao = models.ForeignKey(
        Questao,
        on_delete=models.CASCADE
    )

    opcao_escolhida = models.ForeignKey(
        Opcao,
        on_delete=models.SET_NULL,
        null=True
    )

    acertou = models.BooleanField()
    tempo_em_segundos = models.PositiveIntegerField()

    data_resolucao = models.DateTimeField(auto_now_add=True)

    MODO_CHOICES = [
        ("L", "Lista"),
        ("S", "Simulado"),
    ]

    modo = models.CharField(max_length=1, choices=MODO_CHOICES)

class Simulado(models.Model):

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    concurso = models.ForeignKey(
        Concurso,
        on_delete=models.SET_NULL,
        null=True
    )

    tempo_limite = models.IntegerField()
    pontuacao_final = models.FloatField(null=True, blank=True)

    data_inicio = models.DateTimeField(auto_now_add=True)
    finalizado = models.BooleanField(default=False)