from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from academico.models import Fundamento, Questao, Opcao

class Usuario(AbstractUser):

    TIPO_CHOICES = (
        ("aluno", "Aluno"),
        ("professor", "Professor"),
        ("admin", "Administrador"),
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default="aluno"
    )

    nome_completo = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class PerfilUsuario(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    habilidade_global = models.FloatField(default=0)

    def __str__(self):
        return self.user.username
    
class HabilidadeUsuarioFundamento(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    fundamento = models.ForeignKey(
        Fundamento,
        on_delete=models.CASCADE
    )

    habilidade = models.FloatField(default=0)
    consistencia = models.FloatField(default=0)
    velocidade_media = models.FloatField(default=0)

    class Meta:
        unique_together = ("usuario", "fundamento")

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