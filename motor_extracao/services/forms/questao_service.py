from academico.models import Questao, Opcao


def criar_questao(dados):

    questao = Questao.objects.create(
        texto=dados["enunciado"],
        numero=dados["numero"],
        prova=dados["prova"],
        origem=dados["origem"],
        ano=dados["ano"],
        nivel_sugerido=1000
    )

    for letra, texto in dados["alternativas"].items():

        Opcao.objects.create(
            questao=questao,
            texto=texto,
            correta=(letra == dados["correta"])
        )

    return questao