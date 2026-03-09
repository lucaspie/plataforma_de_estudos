from motor_extracao.services.extractors.pdf_text_extractor import extrair_texto_pdf
from motor_extracao.services.parsers.question_parser import extrair_questoes
from motor_extracao.services.parsers.alternatives_parser import extrair_alternativas
from motor_extracao.services.parsers.answer_parser import extrair_gabarito
from motor_extracao.services.forms.questao_service import criar_questao


def importar_prova(caminho_pdf, prova):

    texto = extrair_texto_pdf(caminho_pdf)

    gabarito = extrair_gabarito(texto)

    questoes = extrair_questoes(texto)

    for q in questoes:

        resultado = extrair_alternativas(q["conteudo"])

        if not resultado:
            continue

        enunciado, alternativas = resultado

        dados = {

            "numero": q["numero"],
            "enunciado": enunciado,
            "alternativas": alternativas,
            "correta": gabarito.get(q["numero"]),
            "prova": prova,
            "origem": prova.nome,
            "ano": prova.ano
        }

        criar_questao(dados)