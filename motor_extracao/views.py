from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from motor_extracao.services.cronogramas.salvar_cronograma import salvar_no_banco
from motor_extracao.services.extractors.pdf_text_extractor import extrair_texto_pdf


@staff_member_required
def importar_cronograma(request):

    if request.method == "POST":

        arquivo = request.FILES.get("arquivo")

        if not arquivo:
            messages.error(request, "Envie um arquivo.")
            return redirect("admin_dashboard")

        try:

            dados = extrair_texto_pdf(arquivo)

            salvar_no_banco(dados)

            messages.success(request, "Conteúdo importado com sucesso.")

        except Exception as e:

            messages.error(request, f"Erro na importação: {e}")

        return redirect("admin_dashboard")

    return redirect("admin_dashboard")