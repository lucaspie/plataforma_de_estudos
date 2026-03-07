from academico.models import Opcao
from avaliacao.models import HistoricoResolucao
from motor.services.tasks import processar_resposta
from analytics.services.propagacao import propagar_habilidade


def processar_lista_questoes(request, questoes):

    resultados = {}
    acertos = 0
    respostas_usuario = {}

    tempo = int(request.POST.get("tempo", 0))

    for q in questoes:

        resposta = request.POST.get(f"q{q.id}")

        if not resposta:
            continue

        resposta = int(resposta)

        opcao = Opcao.objects.filter(id=resposta).first()

        if not opcao:
            continue

        respostas_usuario[q.id] = resposta

        acertou = opcao.correta

        if acertou:
            acertos += 1

        correta = q.opcoes.filter(correta=True).first()

        HistoricoResolucao.objects.create(
            usuario=request.user,
            questao=q,
            opcao_escolhida=opcao,
            acertou=acertou,
            tempo_em_segundos=tempo,
            modo="L"
        )

        processar_resposta.delay(
            request.user.id,
            q.id,
            acertou
        )

        for f in q.fundamentos.all():
            delta = 30 if acertou else -40
            propagar_habilidade(request.user, f, delta)

        resultados[q.id] = {
            "opcao": opcao,
            "acertou": acertou,
            "correta": correta,
        }

    return resultados, acertos, respostas_usuario