import math
from scipy.stats import binom

from django.utils import timezone
from django.db.models import Avg
from django.db.models import Max

from accounts.models import HabilidadeUsuarioFundamento
from academico.models import Questao, Materia
from analytics.models import PrevisaoAprovacao
from avaliacao.models import HistoricoResolucao

#funções de cálculo de probabilidade
def probabilidade_acerto_media(H, D):
    return 1 / (1 + 10 ** ((D - H) / 400))

#funções de rating global do usuário
def rating_global_usuario(usuario):
    habilidades = HabilidadeUsuarioFundamento.objects.filter(usuario=usuario)
    if not habilidades.exists():
        return 0
    return sum(h.habilidade for h in habilidades) / habilidades.count()

def probabilidade_aprovacao(usuario, concurso, total_questoes, corte_percentual):

    H = rating_global_usuario(usuario)
    D = rating_medio_concurso(concurso)

    P = probabilidade_acerto_media(H, D)

    corte = math.ceil(total_questoes * corte_percentual)

    prob = 1 - binom.cdf(corte - 1, total_questoes, P)

    return {
        "probabilidade_aprovacao": round(prob * 100, 2),
        "probabilidade_media_acerto": round(P * 100, 2),
        "rating_usuario": round(H, 2),
        "rating_concurso": round(D, 2),
    }

def rating_medio_concurso(concurso):
    from django.db.models import Avg
    return Questao.objects.filter(
        concurso=concurso
    ).aggregate(Avg("nivel_dinamico"))["nivel_dinamico__avg"] or 0

def obter_ou_atualizar_previsao(usuario, concurso, total_questoes, corte_percentual):

    ultima_resolucao = HistoricoResolucao.objects.filter(
        usuario=usuario
    ).aggregate(Max("data_resolucao"))["data_resolucao__max"]

    if not ultima_resolucao:
        return None

    previsao, created = PrevisaoAprovacao.objects.get_or_create(
        usuario=usuario,
        concurso=concurso,
        defaults={
            "probabilidade_aprovacao": 0,
            "probabilidade_media_acerto": 0,
            "rating_usuario": 0,
            "rating_concurso": 0,
            "ultima_resolucao_processada": ultima_resolucao,
        }
    )

    if created or previsao.ultima_resolucao_processada < ultima_resolucao:

        resultado = probabilidade_aprovacao(
            usuario,
            concurso,
            total_questoes,
            corte_percentual
        )

        previsao.probabilidade_aprovacao = resultado["probabilidade_aprovacao"]
        previsao.probabilidade_media_acerto = resultado["probabilidade_media_acerto"]
        previsao.rating_usuario = resultado["rating_usuario"]
        previsao.rating_concurso = resultado["rating_concurso"]
        previsao.ultima_resolucao_processada = ultima_resolucao

        previsao.save()

    return previsao

#funções de rating por matéria do usuário
def rating_usuario_por_materia(usuario, materia):

    return HabilidadeUsuarioFundamento.objects.filter(
        usuario=usuario,
        fundamento__topico__materia=materia
    ).aggregate(Avg("habilidade"))["habilidade__avg"] or 0

def rating_materia_concurso(concurso, materia):

    return Questao.objects.filter(
        concurso=concurso,
        topico__materia=materia
    ).aggregate(Avg("nivel_dinamico"))["nivel_dinamico__avg"] or 0

def calcular_previsao_por_materia(usuario, concurso, total_questoes_materia, corte_percentual):

    resultados = []

    materias = Materia.objects.filter(
        topicos__questoes__concurso=concurso
    ).distinct()

    for materia in materias:

        H = rating_usuario_por_materia(usuario, materia)
        D = rating_materia_concurso(concurso, materia)

        P = probabilidade_acerto_media(H, D)

        resultados.append({
            "materia": materia,
            "probabilidade_media_acerto": P,
            "rating_usuario": H,
            "rating_materia": D
        })

    return resultados