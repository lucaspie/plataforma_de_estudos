import pdfplumber


def extrair_texto_pdf(caminho_pdf):

    texto = ""

    with pdfplumber.open(caminho_pdf) as pdf:

        for pagina in pdf.pages:
            conteudo = pagina.extract_text()

            if conteudo:
                texto += conteudo + "\n"

    return texto