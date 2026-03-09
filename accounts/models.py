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

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    fundamento = models.ForeignKey(
        Fundamento,
        on_delete=models.CASCADE
    )

    habilidade = models.FloatField(default=900)
    consistencia = models.FloatField(default=0.5)
    velocidade_media = models.FloatField(default=0)

    class Meta:
        unique_together = ("usuario", "fundamento")