from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count, Sum

from .models import Usuario
from .forms import CadastroUsuarioForm, EditarUsuarioForm
from .decorators import role_required
from academico.models import Questao, Concurso, Materia
from avaliacao.models import Simulado, HistoricoResolucao
from analytics.services.diagnostico import diagnostico_usuario
from motor.services.learning_engine import relatorio_completo
from analytics.services.trilha import gerar_trilha_usuario


@login_required
def dashboard(request):

    usuario = request.user

    historico = HistoricoResolucao.objects.filter(usuario=usuario)
    trilha = gerar_trilha_usuario(request.user)

    total_resolvidas = historico.count()
    total_acertos = historico.filter(acertou=True).count()

    taxa_acerto = 0
    if total_resolvidas > 0:
        taxa_acerto = round((total_acertos / total_resolvidas) * 100)

    diagnostico = relatorio_completo(usuario)

    progresso_materias = (
        historico
        .select_related("questao__topico__materia")
        .values("questao__topico__materia__nome")
        .annotate(
            resolvidas=Count("id"),
            acertos=Sum("acertou")
        )
    )

    materias = []

    for m in progresso_materias:

        resolvidas = m["resolvidas"]
        acertos = m["acertos"] or 0

        percentual = 0

        if resolvidas > 0:
            percentual = round((acertos / resolvidas) * 100)

        materias.append({
            "nome": m["questao__topico__materia__nome"],
            "percentual": percentual
        })

    context = {
        "total_resolvidas": total_resolvidas,
        "taxa_acerto": taxa_acerto,
        "materias": materias,
        "diagnostico": diagnostico,
        "trilha": trilha
    }

    return render(request, "accounts/dashboard.html", context)


@login_required
@role_required("admin")
def admin_dashboard(request):

    usuarios_list = Usuario.objects.all().order_by('-id')

    usuario = request.GET.get("usuario")
    if usuario:
        usuarios_list = usuarios_list.filter(
            Q(username__icontains=usuario) |
            Q(nome_completo__icontains=usuario) |
            Q(email__icontains=usuario)
        )

    total_usuarios = usuarios_list.count()
    total_questoes = Questao.objects.count()
    total_simulados = Simulado.objects.count()
    total_concursos = Concurso.objects.count()
    total_materias = Materia.objects.count()

    paginator = Paginator(usuarios_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "accounts/admin_dashboard.html", {
        "usuarios": page_obj,
        "page_obj": page_obj,
        "total_usuarios": total_usuarios,
        "filtros": request.GET,
        "total_questoes": total_questoes,
        "total_simulados": total_simulados,
        "total_concursos": total_concursos,
        "total_materias": total_materias,
    })


def cadastro(request):

    if request.method == "POST":
        form = CadastroUsuarioForm(request.POST)

        if form.is_valid():
            user = form.save()

            authenticated_user = authenticate(
                request,
                username=user.username,
                password=form.cleaned_data["password1"],
            )

            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect("redirect_after_login")

            else:
                form.add_error(None, "Erro ao autenticar usuário recém-criado.")

    else:
        form = CadastroUsuarioForm()

    return render(request, "accounts/cadastro.html", {"form": form})


@login_required
@role_required("admin")
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == "POST":
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso.")
            return redirect("lista_usuarios")
    else:
        form = EditarUsuarioForm(instance=usuario)

    return render(request, "accounts/editar_usuario.html", {
        "form": form,
        "usuario": usuario
    })


@login_required
@role_required("admin")
def toggle_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    usuario.is_active = not usuario.is_active
    usuario.save()
    return redirect("admin_dashboard")


@login_required
def redirect_after_login(request):
    user = request.user

    if user.is_staff or user.is_superuser:
        return redirect("admin_dashboard")
    else:
        return redirect("dashboard")