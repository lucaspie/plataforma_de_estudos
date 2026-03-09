from academico.models import Materia, Topico
from motor_extracao.services.classifiers.materia_classifier import classificar_materia
from motor_extracao.services.classifiers.topico_classifier import classificar_topico


def classificar_questao(questao):

    texto = questao.texto

    nome_materia = classificar_materia(texto)
    nome_topico = classificar_topico(texto)

    if nome_materia:

        materia = Materia.objects.filter(nome=nome_materia).first()

        if materia:
            questao.materia = materia

    if nome_topico:

        topico = Topico.objects.filter(nome=nome_topico).first()

        if topico:
            questao.topico = topico

    questao.save()