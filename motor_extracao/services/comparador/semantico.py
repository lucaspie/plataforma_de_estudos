from motor_extracao.services.semantica.similaridade import similaridade_semantica


def encontrar_semelhante(nome, queryset, limite=0.80):

    melhor = None
    melhor_score = 0

    for obj in queryset:

        score = similaridade_semantica(nome, obj.nome)

        if score > limite and score > melhor_score:

            melhor = obj
            melhor_score = score

    return melhor