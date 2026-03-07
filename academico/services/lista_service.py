from motor.services.learning_engine import gerar_sessao_adaptativa


def gerar_lista(usuario, queryset_base, quantidade=20):
    return gerar_sessao_adaptativa(usuario, queryset_base, quantidade)