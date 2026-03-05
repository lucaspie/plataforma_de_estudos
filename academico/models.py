from django.db import models

class Concurso(models.Model):
    nome = models.CharField(max_length=150)
    banca = models.CharField(max_length=150)
    ano = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.banca}"
    
class Materia(models.Model):
    nome = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.nome
    
class Topico(models.Model):
    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE,
        related_name="topicos"
    )
    nome = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.materia.nome} > {self.nome}"
    
class Fundamento(models.Model):
    topico = models.ForeignKey(
        Topico,
        on_delete=models.CASCADE,
        related_name="fundamentos"
    )
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)

    peso_relevancia = models.FloatField(
        default=1.0,
        help_text="Impacto do fundamento na dificuldade real"
    )

    def __str__(self):
        return f"{self.topico.nome} - {self.nome}"
    
class Questao(models.Model):

    concurso = models.ForeignKey(
        Concurso,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="questoes"
    )

    topico = models.ForeignKey(
        Topico,
        on_delete=models.PROTECT,
        related_name="questoes"
    )

    fundamentos = models.ManyToManyField(
        Fundamento,
        related_name="questoes"
    )

    texto = models.TextField()
    imagem = models.ImageField(upload_to="questoes/", null=True, blank=True)

    origem = models.CharField(max_length=150, db_index=True)
    ano = models.IntegerField(null=True, blank=True)

    # Níveis
    nivel_sugerido = models.IntegerField()
    nivel_dinamico = models.FloatField(null=True, blank=True)

    # Estatísticas globais
    total_respostas = models.PositiveIntegerField(default=0)
    total_acertos = models.PositiveIntegerField(default=0)

    indice_discriminacao = models.FloatField(default=0)

    resolucao_mestra = models.TextField(blank=True)

    data_criacao = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.nivel_dinamico is None:
            self.nivel_dinamico = self.nivel_sugerido
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.topico.nome} - Nível {self.nivel_dinamico}"
    
class Opcao(models.Model):
    questao = models.ForeignKey(
        Questao,
        on_delete=models.CASCADE,
        related_name="opcoes"
    )

    texto = models.TextField()
    correta = models.BooleanField(default=False)
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f"Questão {self.questao.id} - {'Correta' if self.correta else 'Errada'}"