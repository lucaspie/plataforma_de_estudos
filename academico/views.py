import json

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .models import Concurso, Materia, Topico, Fundamento, Questao, Opcao, DependenciaFundamento
from avaliacao.models import HistoricoResolucao
from .forms import ConcursoForm, MateriaForm, TopicoForm, FundamentoForm, QuestaoForm, OpcaoFormSet, OpcaoForm

from accounts.decorators import role_required
from .mixin import RoleRequiredMixin
from academico.services.questoes_service import processar_lista_questoes
from academico.services.lista_service import gerar_lista
from motor.services.seletor_inteligente import selecionar_questoes_adaptativas
from analytics.services.relatorio import relatorio_materia
from analytics.services.trilha import gerar_trilha_usuario
from motor_extracao.services.cronogramas.salvar_cronograma import salvar_no_banco
from motor_extracao.services.extractors.pdf_text_extractor import extrair_texto_pdf

#Parte do concurso
class ConcursoListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Concurso
    template_name = "academico/concurso_list.html"
    context_object_name = "concursos"
    required_role = "admin"
    ordering = ["nome"]
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()

        busca = self.request.GET.get("buscar")

        if busca:
            qs = qs.filter(nome__icontains=busca)

        return qs


class ConcursoCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Concurso
    form_class = ConcursoForm
    template_name = "academico/form.html"
    success_url = reverse_lazy("concurso_list")
    required_role = "admin"


class ConcursoUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Concurso
    form_class = ConcursoForm
    template_name = "academico/form.html"
    success_url = reverse_lazy("concurso_list")
    required_role = "admin"


class ConcursoDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Concurso
    template_name = "academico/confirm_delete.html"
    success_url = reverse_lazy("concurso_list")
    required_role = "admin"


#parte da matéria
class MateriaListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Materia
    template_name = "academico/materia_list.html"
    context_object_name = "materias"
    required_role = "admin"
    ordering = ["nome"]
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()

        busca = self.request.GET.get("buscar")

        if busca:
            qs = qs.filter(nome__icontains=busca)

        return qs


class MateriaCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Materia
    form_class = MateriaForm
    template_name = "academico/form.html"
    success_url = reverse_lazy("materia_list")
    required_role = "admin"


class MateriaUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Materia
    form_class = MateriaForm
    template_name = "academico/form.html"
    success_url = reverse_lazy("materia_list")
    required_role = "admin"


class MateriaDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Materia
    template_name = "academico/confirm_delete.html"
    success_url = reverse_lazy("materia_list")
    required_role = "admin"


#parte do tópico
class TopicoListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Topico
    template_name = "academico/topico_list.html"
    context_object_name = "topicos"
    required_role = "admin"
    ordering = ["nome"]
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()

        busca = self.request.GET.get("buscar")

        if busca:
            qs = qs.filter(nome__icontains=busca)

        return qs


class TopicoCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Topico
    form_class = TopicoForm
    template_name = "academico/form.html"
    success_url = reverse_lazy("topico_list")
    required_role = "admin"


class TopicoUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Topico
    form_class = TopicoForm
    template_name = "academico/form.html"
    success_url = reverse_lazy("topico_list")
    required_role = "admin"


class TopicoDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Topico
    template_name = "academico/confirm_delete.html"
    success_url = reverse_lazy("topico_list")
    required_role = "admin"

#parte do fundamento
class FundamentoListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Fundamento
    template_name = "academico/fundamento_list.html"
    context_object_name = "fundamentos"
    required_role = "admin"
    ordering = ["nome"]
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()

        busca = self.request.GET.get("buscar")

        if busca:
            qs = qs.filter(nome__icontains=busca)

        return qs


class FundamentoCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Fundamento
    form_class = FundamentoForm
    template_name = "academico/form.html"
    success_url = reverse_lazy("fundamento_list")
    required_role = "admin"


class FundamentoUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Fundamento
    form_class = FundamentoForm
    template_name = "academico/form.html"
    success_url = reverse_lazy("fundamento_list")
    required_role = "admin"


class FundamentoDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Fundamento
    template_name = "academico/confirm_delete.html"
    success_url = reverse_lazy("fundamento_list")
    required_role = "admin"

#parte das questões
@login_required
@role_required("admin")
def create_questao(request):

    if request.method == "POST":
        form = QuestaoForm(request.POST, request.FILES)
        formset = OpcaoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            questao = form.save()

            opcoes = formset.save(commit=False)
            for opcao in opcoes:
                opcao.questao = questao
                opcao.save()

            return redirect("questao_list")

        else:
            print("ERROS FORM:", form.errors)
            print("ERROS FORMSET:", formset.errors)

    else:
        form = QuestaoForm()
        formset = OpcaoFormSet()

    return render(request, "academico/form.html", {
        "form": form,
        "formset": formset
    })


class QuestaoListView(ListView):
    model = Questao
    paginate_by = 20
    template_name = "academico/questao_list.html"
    context_object_name = "questoes"
    required_role = "admin"

    def get_queryset(self):
        qs = super().get_queryset().select_related("topico", "concurso")

        topico = self.request.GET.get("topico")
        busca = self.request.GET.get("usuario")

        if topico:
            qs = qs.filter(topico_id=topico)

        if busca:
            qs = qs.filter(
                Q(texto__icontains=busca) |
                Q(origem__icontains=busca) |
                Q(topico__nome__icontains=busca)
            )

        return qs

class QuestaoUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Questao
    form_class = QuestaoForm
    template_name = "academico/form.html"
    success_url = reverse_lazy("questao_list")
    required_role = "admin"


class QuestaoDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Questao
    template_name = "academico/confirm_delete.html"
    success_url = reverse_lazy("questao_list")
    required_role = "admin"


#parte das opções
class OpcaoListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Opcao
    template_name = "academico/opcao_list.html"
    context_object_name = "opcoes"
    required_role = "admin"
    ordering = ["texto"]
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()

        busca = self.request.GET.get("buscar")

        if busca:
            qs = qs.filter(nome__icontains=busca)

        return qs


class OpcaoCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Opcao
    form_class = OpcaoForm
    template_name = "academico/form.html"
    success_url = reverse_lazy("opcao_list")
    required_role = "admin"


class OpcaoUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Opcao
    form_class = OpcaoForm
    template_name = "academico/form.html"
    success_url = reverse_lazy("opcao_list")
    required_role = "admin"


class OpcaoDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Opcao
    template_name = "academico/confirm_delete.html"
    success_url = reverse_lazy("opcao_list")
    required_role = "admin"


#Parte do skill graph
class DependenciaFundamentoCreateView(CreateView):
    model = DependenciaFundamento
    fields = ["fundamento", "prerequisito", "peso"]
    template_name = "academico/form.html"
    success_url = reverse_lazy("skill_graph_list")


class DependenciaFundamentoListView(ListView):
    model = DependenciaFundamento
    template_name = "academico/skill_graph_list.html"
    context_object_name = "dependencias"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related(
            "fundamento__topico__materia",
            "prerequisito__topico__materia"
        )

        fundamento_id = self.request.GET.get("fundamento")
        busca = self.request.GET.get("buscar")
        materia_id = self.request.GET.get("materia")
        topico_id = self.request.GET.get("topico")

        if materia_id:
            qs = qs.filter(
                fundamento__topico__materia_id=materia_id
            )

        if topico_id:
            qs = qs.filter(
                fundamento__topico_id=topico_id
            )

        if fundamento_id:
            qs = qs.filter(fundamento_id=fundamento_id)

        if busca:
            qs = qs.filter(fundamento__nome__icontains=busca)

        return qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        materia_id = self.request.GET.get("materia")
        topico_id = self.request.GET.get("topico")

        context["materias"] = Materia.objects.all()

        context["topicos"] = (
            Topico.objects.filter(materia_id=materia_id)
            if materia_id else Topico.objects.none()
        )

        context["fundamentos"] = (
            Fundamento.objects.filter(topico_id=topico_id)
            if topico_id else Fundamento.objects.none()
        )

        context["materia_selected"] = materia_id
        context["topico_selected"] = topico_id
        context["fundamento_selected"] = self.request.GET.get("fundamento")

        return context


class DependenciaFundamentoUpdateView(UpdateView):
    model = DependenciaFundamento
    fields = ["fundamento", "prerequisito", "peso"]
    template_name = "academico/form.html"
    success_url = reverse_lazy("skill_graph_list")


class DependenciaFundamentoDeleteView(DeleteView):
    model = DependenciaFundamento
    template_name = "academico/confirm_delete.html"
    success_url = reverse_lazy("skill_graph_list")


class SkillGraphView(TemplateView):
    template_name = "academico/skill_graph_visualizacao.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        materia_id = self.request.GET.get("materia")
        topico_id = self.request.GET.get("topico")

        dependencias = DependenciaFundamento.objects.select_related(
            "fundamento__topico__materia",
            "prerequisito__topico__materia"
        )

        # FILTRO POR MATÉRIA
        if materia_id:
            dependencias = dependencias.filter(
                fundamento__topico__materia_id=materia_id
            )

        # FILTRO POR TÓPICO
        if topico_id:
            dependencias = dependencias.filter(
                fundamento__topico_id=topico_id
            )

        nodes = {}
        edges = []

        for d in dependencias:

            nodes[d.fundamento.id] = d.fundamento.nome
            nodes[d.prerequisito.id] = d.prerequisito.nome

            edges.append({
                "source": d.prerequisito.id,
                "target": d.fundamento.id,
                "peso": d.peso
            })

        context["nodes"] = [
            {"id": k, "label": v}
            for k, v in nodes.items()
        ]

        context["edges"] = edges

        # dados para filtros
        context["materias"] = Materia.objects.all()
        context["topicos"] = Topico.objects.filter(
            materia_id=materia_id
        ) if materia_id else Topico.objects.none()

        context["materia_selected"] = materia_id
        context["topico_selected"] = topico_id

        return context


#-----------------------------------    Parte do aluno
@login_required
def materias_list_alunos(request):
    materias = Materia.objects.all().order_by("nome")

    return render(request, "aluno/materias.html", {
        "materias": materias
    })


@login_required
def materia_detail_alunos(request, pk):

    materia = get_object_or_404(Materia, pk=pk)

    busca = request.GET.get("q")

    topicos_list = Topico.objects.filter(
        materia=materia
    ).prefetch_related("fundamentos")

    relatorio = relatorio_materia(request.user, materia)
    trilha = gerar_trilha_usuario(request.user)

    # busca dinâmica
    if busca:
        topicos_list = topicos_list.filter(
            Q(nome__icontains=busca) |
            Q(fundamentos__nome__icontains=busca)
        ).distinct()

    paginator = Paginator(topicos_list.order_by("nome"), 1)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "aluno/materia_detail.html", {
        "materia": materia,
        "page_obj": page_obj,
        "topicos": page_obj.object_list,
        "busca": busca,
        "relatorio": relatorio,
        "mapa_json": json.dumps(relatorio["mapa"]),
        "trilha": trilha
    })


@login_required
def gerar_lista_materia_alunos(request, pk):

    materia = get_object_or_404(Materia, pk=pk)

    base = Questao.objects.filter(
        topico__materia=materia
    )

    questoes = gerar_lista(request.user, base)

    if request.method == "POST":

        resultados, acertos, respostas_usuario = processar_lista_questoes(request, questoes)

        return render(request, "aluno/lista_questoes.html", {
            "questoes": questoes,
            "titulo": f"Questões de {materia.nome}",
            "resultados": resultados,
            "acertos": acertos,
            "total": len(questoes),
            "respostas_usuario": respostas_usuario
        })

    return render(request, "aluno/lista_questoes.html", {
        "questoes": questoes,
        "titulo": f"Questões de {materia.nome}"
    })


@login_required
def gerar_lista_topico_alunos(request, pk):

    topico = get_object_or_404(Topico, pk=pk)

    base = Questao.objects.filter(
        topico=topico
    )

    questoes = gerar_lista(request.user, base)

    if request.method == "POST":

        resultados, acertos, respostas_usuario = processar_lista_questoes(request, questoes)

        return render(request, "aluno/lista_questoes.html", {
            "questoes": questoes,
            "titulo": f"Questões de {topico.nome}",
            "resultados": resultados,
            "acertos": acertos,
            "total": len(questoes),
            "respostas_usuario": respostas_usuario
        })

    return render(request, "aluno/lista_questoes.html", {
        "questoes": questoes,
        "titulo": f"Questões de {topico.nome}"
    })


@login_required
def gerar_lista_fundamento_alunos(request, pk):

    fundamento = get_object_or_404(Fundamento, pk=pk)

    base = Questao.objects.filter(
        fundamentos=fundamento
    )

    questoes = gerar_lista(request.user, base)

    if request.method == "POST":

        resultados, acertos, respostas_usuarios = processar_lista_questoes(request, questoes)

        return render(request, "aluno/lista_questoes.html", {
            "questoes": questoes,
            "titulo": f"Questões de {fundamento.nome}",
            "resultados": resultados,
            "acertos": acertos,
            "total": len(questoes),
            "respostas_usuario": respostas_usuarios
        })

    return render(request, "aluno/lista_questoes.html", {
        "questoes": questoes,
        "titulo": f"Questões de {fundamento.nome}"
    })


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