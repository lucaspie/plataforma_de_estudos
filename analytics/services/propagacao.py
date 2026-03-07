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

        fator = 1 / (nivel + 1)

        habilidade = HabilidadeUsuarioFundamento.objects.filter(
            usuario=usuario,
            fundamento=atual
        ).first()

        if habilidade:

            habilidade.habilidade += delta * fator
            habilidade.habilidade = max(0, min(1000, habilidade.habilidade))
            habilidade.save()

        dependencias = DependenciaFundamento.objects.filter(
            fundamento=atual
        )

        for d in dependencias:

            fila.append((d.prerequisito, nivel + 1))