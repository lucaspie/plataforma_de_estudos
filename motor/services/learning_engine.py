from collections import defaultdict
from django.utils import timezone
from datetime import timedelta
import random

from django.db.models import FloatField, ExpressionWrapper, Case, When, Value, F

from academico.models import Questao
from avaliacao.models import HistoricoResolucao
from analytics.models import MemoriaFundamento
from accounts.models import HabilidadeUsuarioFundamento

from analytics.services.skill_graph import obter_prerequisitos

def calcular_desempenho_por_fundamento(usuario):

    respostas = HistoricoResolucao.objects.filter(usuario=usuario)

    stats = defaultdict(lambda: {"acertos":0, "total":0})

    for r in respostas:

        fundamentos = r.questao.fundamentos.all()

        for f in fundamentos:

            stats[f.id]["total"] += 1

            if r.acertou:
                stats[f.id]["acertos"] += 1


    desempenho = {}

    for f, v in stats.items():

        taxa = 0

        if v["total"] > 0:
            taxa = v["acertos"] / v["total"]

        desempenho[f] = taxa


    return desempenho


def detectar_fraquezas(usuario):

    desempenho = calcular_desempenho_por_fundamento(usuario)

    fracos = []
    medios = []
    fortes = []

    for fundamento, taxa in desempenho.items():

        if taxa < 0.5:
            fracos.append(fundamento)

        elif taxa < 0.75:
            medios.append(fundamento)

        else:
            fortes.append(fundamento)

    return fracos, medios, fortes


def calcular_distribuicao(total, fracos, medios, fortes):

    qtd_fracos = int(total * 0.5)
    qtd_medios = int(total * 0.3)
    qtd_fortes = total - qtd_fracos - qtd_medios

    return qtd_fracos, qtd_medios, qtd_fortes


def filtrar_questoes_recentes(usuario, qs):

    limite = timezone.now() - timedelta(days=3)

    recentes = HistoricoResolucao.objects.filter(
        usuario=usuario,
        data_resolucao__gte=limite
    ).values_list("questao_id", flat=True)

    return qs.exclude(id__in=recentes)


def questoes_erradas(usuario):

    return Questao.objects.filter(
        historico__usuario=usuario,
        historico__acertou=False
    ).distinct()


def questoes_erradas_recentes(usuario, limite=5):

    limite_data = timezone.now() - timedelta(days=7)

    erros = HistoricoResolucao.objects.filter(
        usuario=usuario,
        acertou=False,
        data_resolucao__gte=limite_data
    ).values_list("questao_id", flat=True)

    return list(
        Questao.objects.filter(id__in=erros).distinct()[:limite]
    )


def selecionar_por_fundamento(fundamentos, quantidade):

    qs = Questao.objects.filter(
        fundamentos__id__in=fundamentos
    ).distinct()

    qs = list(qs)

    random.shuffle(qs)

    return qs[:quantidade]


def revisoes_pendentes(usuario, limite=5):

    fundamentos = MemoriaFundamento.objects.filter(
        usuario=usuario,
        proxima_revisao__lte=timezone.now()
    ).values_list("fundamento_id", flat=True)

    qs = Questao.objects.filter(
        fundamentos__id__in=fundamentos
    ).distinct()

    return list(qs[:limite])


def dificuldade_alvo(usuario, fundamentos):

    habilidades = HabilidadeUsuarioFundamento.objects.filter(
        usuario=usuario,
        fundamento__id__in=fundamentos
    )

    if not habilidades.exists():
        return 0

    media = sum(h.habilidade for h in habilidades) / habilidades.count()

    return media


def selecionar_por_dificuldade(fundamentos, habilidade, quantidade):

    margem = max(100, habilidade * 0.2)

    qs = Questao.objects.filter(
        fundamentos__id__in=fundamentos,
        nivel_dinamico__gte=habilidade - margem,
        nivel_dinamico__lte=habilidade + margem
    ).distinct()

    qs = list(qs)

    random.shuffle(qs)

    return qs[:quantidade]


def explorar_questoes_novas(base, sessao, quantidade=3):

    usadas = [q.id for q in sessao]

    qs = base.exclude(id__in=usadas).order_by("?")

    return list(qs[:quantidade])


def fundamentos_dominados(usuario):

    habilidades = HabilidadeUsuarioFundamento.objects.filter(usuario=usuario)

    dominados = []

    for h in habilidades:

        if h.habilidade > 800:
            dominados.append(h.fundamento__id)

    return dominados


def questoes_dificeis(base):

    qs = base.annotate(
        taxa_erro=Case(
            When(total_respostas=0, then=Value(0)),
            default=ExpressionWrapper(
                1 - (F("total_acertos") * 1.0 / F("total_respostas")),
                output_field=FloatField()
            )
        )
    ).order_by("-taxa_erro")

    return qs

def gerar_sessao_adaptativa(usuario, queryset_base, total=20):

    base = filtrar_questoes_recentes(usuario, queryset_base)

    total = min(total, base.count())

    sessao = []

    # 1️⃣ Revisões ANKI
    revisoes = revisoes_pendentes(usuario, 5)

    revisoes = base.filter(id__in=[q.id for q in revisoes])

    sessao += list(revisoes)

    # 2️⃣ Erros recentes
    erros = questoes_erradas_recentes(usuario, 5)

    erros = base.filter(id__in=[q.id for q in erros])

    sessao += list(erros)

    restantes = total - len(sessao)

    if restantes <= 0:
        random.shuffle(sessao)
        return sessao[:total]

    # 3️⃣ Diagnóstico
    fracos, medios, fortes = detectar_fraquezas(usuario)

    fracos, medios, fortes = detectar_fraquezas(usuario)

    fundamentos_expandidos = set(fracos)

    for f in fracos:

        prereqs = obter_prerequisitos(f)

        for p in prereqs:
            fundamentos_expandidos.add(p)

    fracos = list(fundamentos_expandidos)

    qf, qm, qfortes = calcular_distribuicao(
        restantes,
        fracos,
        medios,
        fortes
    )

    # 4️⃣ Seleção adaptativa

    if fracos:

        habilidade = dificuldade_alvo(usuario, fracos)

        qs_fracos = base.filter(
            fundamentos__id__in=fracos,
            nivel_dinamico__gte=habilidade-150,
            nivel_dinamico__lte=habilidade+150
        ).distinct()

        sessao += random.sample(list(qs_fracos), min(qf, qs_fracos.count()))

    if medios:

        habilidade = dificuldade_alvo(usuario, medios)

        qs_medios = base.filter(
            fundamentos__id__in=medios,
            nivel_dinamico__gte=habilidade-150,
            nivel_dinamico__lte=habilidade+150
        ).distinct()

        sessao += random.sample(list(qs_medios), min(qm, qs_medios.count()))

    if fortes:

        habilidade = dificuldade_alvo(usuario, fortes)

        qs_fortes = base.filter(
            fundamentos__id__in=fortes,
            nivel_dinamico__gte=habilidade-1,
            nivel_dinamico__lte=habilidade+1
        ).distinct()

        sessao += random.sample(list(qs_fortes), min(qfortes, qs_fortes.count()))


    dominados = fundamentos_dominados(usuario)
    fortes = [f for f in fortes if f not in dominados]
    random.shuffle(sessao)
    sessao = list(dict.fromkeys(sessao))

    if len(sessao) == 0:
        return list(base.order_by("?")[:total])
    
    dificeis = questoes_dificeis(base.filter(fundamentos__id__in=dominados))

    dificeis = dificeis.exclude(id__in=[q.id for q in sessao])[:3]
    sessao += list(dificeis)
    
    exploracao = explorar_questoes_novas(base, sessao, 3)
    sessao += exploracao

    return sessao[:total]


def relatorio_completo(user):

    historico = HistoricoResolucao.objects.filter(usuario=user)\
        .select_related("questao__topico__materia")\
        .prefetch_related("questao__fundamentos")

    stats = defaultdict(lambda: {
        "materia": "",
        "topico": "",
        "fundamento": "",
        "acertos": 0,
        "total": 0
    })

    for r in historico:

        q = r.questao
        materia = q.topico.materia.nome
        topico = q.topico.nome

        for f in q.fundamentos.all():

            chave = f.id

            stats[chave]["materia"] = materia
            stats[chave]["topico"] = topico
            stats[chave]["fundamento"] = f.nome
            stats[chave]["total"] += 1

            if r.acertou:
                stats[chave]["acertos"] += 1

    fracos = []
    medios = []
    fortes = []
    ratings = []

    for s in stats.values():

        total = s["total"]
        acertos = s["acertos"]

        taxa = acertos / total if total > 0 else 0

        rating = int(300 + taxa * 700)

        ratings.append(rating)

        registro = {
            "materia": s["materia"],
            "topico": s["topico"],
            "fundamento": s["fundamento"],
            "rating": rating,
            "acerto": int(taxa * 100),
            "total": total
        }

        if rating < 500:
            fracos.append(registro)

        elif rating < 700:
            medios.append(registro)

        else:
            fortes.append(registro)

    nivel_global = int(sum(ratings) / len(ratings)) if ratings else 0

    if nivel_global < 500:
        nivel_texto = "Iniciante"
    elif nivel_global < 700:
        nivel_texto = "Intermediário"
    else:
        nivel_texto = "Avançado"

    fracos.sort(key=lambda x: x["rating"])
    fortes.sort(key=lambda x: -x["rating"])

    return {
        "fundamentos_fracos": fracos[:10],
        "fundamentos_medios": medios[:10],
        "fundamentos_fortes": fortes[:10],
        "nivel_texto": nivel_texto,
        "nivel_global": nivel_global
    }