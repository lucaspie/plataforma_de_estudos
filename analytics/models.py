from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from academico.models import Concurso, Materia

class PrevisaoAprovacao(models.Model):

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    concurso = models.ForeignKey(
        Concurso,
        on_delete=models.CASCADE
    )

    probabilidade_aprovacao = models.FloatField()
    probabilidade_media_acerto = models.FloatField()
    rating_usuario = models.FloatField()
    rating_concurso = models.FloatField()

    ultima_resolucao_processada = models.DateTimeField()
    data_calculo = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("usuario", "concurso")

class PrevisaoMateria(models.Model):

    previsao = models.ForeignKey(
        "PrevisaoAprovacao",
        on_delete=models.CASCADE,
        related_name="materias"
    )

    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE
    )

    probabilidade_aprovacao = models.FloatField()
    probabilidade_media_acerto = models.FloatField()
    rating_usuario = models.FloatField()
    rating_materia = models.FloatField()

    class Meta:
        unique_together = ("previsao", "materia")

class MemoriaFundamento(models.Model):

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    fundamento = models.ForeignKey(
        "academico.Fundamento",
        on_delete=models.CASCADE
    )

    intervalo = models.FloatField(default=1)

    repeticoes = models.IntegerField(default=0)

    facilidade = models.FloatField(default=2.5)

    proxima_revisao = models.DateTimeField()

    ultima_resposta = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("usuario", "fundamento")