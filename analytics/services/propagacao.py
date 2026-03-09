from academico.models import DependenciaFundamento
from accounts.models import HabilidadeUsuarioFundamento


def propagar_habilidade(usuario, fundamento, delta):

    visitados = set()
    fila = [(fundamento, 0)]

    while fila:

        atual, nivel = fila.pop(0)

        if atual.id in visitados:
            continue

        visitados.add(atual.id)

        fator = 0.6 ** nivel

        habilidade = HabilidadeUsuarioFundamento.objects.filter(
            usuario=usuario,
            fundamento=atual
        ).first()

        if habilidade:

            habilidade.habilidade += delta * fator
            habilidade.habilidade = max(100, min(2000, habilidade.habilidade))
            habilidade.save()

        dependencias = DependenciaFundamento.objects.filter(
            fundamento=atual
        )

        for d in dependencias:

            fila.append((d.prerequisito, nivel + 1))