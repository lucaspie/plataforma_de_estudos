from avaliacao.models import HistoricoResolucao
from academico.models import Opcao


def processar_lista_questoes(request, questoes):

    resultados = {}
    acertos = 0

    for q in questoes:

        resposta = request.POST.get(f"q{q.id}")

        if not resposta:
            continue

        opcao = Opcao.objects.get(id=resposta)

        acertou = opcao.correta

        if acertou:
            acertos += 1

        HistoricoResolucao.objects.create(
            usuario=request.user,
            questao=q,
            opcao_escolhida=opcao,
            acertou=acertou,
            tempo_em_segundos=request.POST.get("tempo", 0),
            modo="L"
        )

        resultados[q.id] = {
            "opcao": opcao,
            "acertou": acertou,
            "correta": q.opcoes.filter(correta=True).first()
        }

    return resultados, acertos