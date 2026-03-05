from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Concurso, Materia, Topico, Fundamento, Questao, Opcao
from .forms import ConcursoForm, MateriaForm, TopicoForm, FundamentoForm, QuestaoForm, OpcaoFormSet, OpcaoForm
from accounts.decorators import role_required
from .mixin import RoleRequiredMixin

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
        "busca": busca
    })


@login_required
def gerar_lista_materia_alunos(request, pk):

    materia = get_object_or_404(Materia, pk=pk)

    questoes = Questao.objects.filter(
        topico__materia=materia
    ).distinct()

    return render(request, "aluno/lista_questoes.html", {
        "questoes": questoes,
        "titulo": f"Questões de {materia.nome}"
    })


@login_required
def gerar_lista_topico_alunos(request, pk):

    topico = get_object_or_404(Topico, pk=pk)

    questoes = Questao.objects.filter(
        topico=topico
    )

    return render(request, "aluno/lista_questoes.html", {
        "questoes": questoes,
        "titulo": f"Questões de {topico.nome}"
    })


@login_required
def gerar_lista_fundamento_alunos(request, pk):

    fundamento = get_object_or_404(Fundamento, pk=pk)

    questoes = Questao.objects.filter(
        fundamentos=fundamento
    )

    return render(request, "aluno/lista_questoes.html", {
        "questoes": questoes,
        "titulo": f"Questões de {fundamento.nome}"
    })