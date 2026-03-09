from academico.models import DependenciaFundamento


def obter_prerequisitos(fundamento_id, profundidade=2):

    visitados = set()
    fila = [(fundamento_id, 0)]

    prereqs = []

    while fila:

        atual, nivel = fila.pop(0)

        if nivel >= profundidade:
            continue

        deps = DependenciaFundamento.objects.filter(
            fundamento_id=atual
        )

        for d in deps:

            if d.prerequisito_id not in visitados:

                visitados.add(d.prerequisito_id)

                prereqs.append(d.prerequisito_id)  # ← mudança

                fila.append((d.prerequisito_id, nivel + 1))

    return prereqs