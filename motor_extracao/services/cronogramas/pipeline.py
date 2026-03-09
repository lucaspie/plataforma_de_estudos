from motor_extracao.services.cronogramas.normalizador import normalizar_linhas
from motor_extracao.services.cronogramas.parser_robusto import extrair_estrutura


def extrator_edital(texto):

    linhas = normalizar_linhas(texto)

    materias = extrair_estrutura(linhas)

    return materias