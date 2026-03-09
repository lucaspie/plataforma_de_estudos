from django.urls import path
from . import views

urlpatterns = [
    path("concursos/", views.ConcursoListView.as_view(), name="concurso_list"),
    path("concursos/novo/", views.ConcursoCreateView.as_view(), name="concurso_create"),
    path("concursos/<int:pk>/editar/",views.ConcursoUpdateView.as_view(), name="concurso_update"),
    path("concursos/<int:pk>/deletar/", views.ConcursoDeleteView.as_view(), name="concurso_delete"),

    path("materias/", views.MateriaListView.as_view(), name="materia_list"),
    path("materias/novo/", views.MateriaCreateView.as_view(), name="materia_create"),
    path("materias/<int:pk>/editar/",views.MateriaUpdateView.as_view(), name="materia_update"),
    path("materias/<int:pk>/deletar/", views.MateriaDeleteView.as_view(), name="materia_delete"),

    path("topicos/", views.TopicoListView.as_view(), name="topico_list"),
    path("topicos/novo/", views.TopicoCreateView.as_view(), name="topico_create"),
    path("topicos/<int:pk>/editar/",views.TopicoUpdateView.as_view(), name="topico_update"),
    path("topicos/<int:pk>/deletar/", views.TopicoDeleteView.as_view(), name="topico_delete"),

    path("fundamentos/", views.FundamentoListView.as_view(), name="fundamento_list"),
    path("fundamentos/novo/", views.FundamentoCreateView.as_view(), name="fundamento_create"),
    path("fundamentos/<int:pk>/editar/",views.FundamentoUpdateView.as_view(), name="fundamento_update"),
    path("fundamentos/<int:pk>/deletar/", views.FundamentoDeleteView.as_view(), name="fundamento_delete"),

    path("questoes/", views.QuestaoListView.as_view(), name="questao_list"),
    path("questoes/nova/", views.create_questao, name="questao_create"),
    path("questoes/<int:pk>/editar/",views.QuestaoUpdateView.as_view(), name="questao_update"),
    path("questoes/<int:pk>/deletar/", views.QuestaoDeleteView.as_view(), name="questao_delete"),

    path("opcoes/", views.OpcaoListView.as_view(), name="opcao_list"),
    path("opcoes/novo/", views.OpcaoCreateView.as_view(), name="opcao_create"),
    path("opcoes/<int:pk>/editar/",views.OpcaoUpdateView.as_view(), name="opcao_update"),
    path("opcoes/<int:pk>/deletar/", views.OpcaoDeleteView.as_view(), name="opcao_delete"),


    path("skill-graph/visualizacao/", views.SkillGraphView.as_view(), name="skill_graph_visualizacao"),
    path("skill-graph/", views.DependenciaFundamentoListView.as_view(), name="skill_graph_list"),
    path("skill-graph/criar/", views.DependenciaFundamentoCreateView.as_view(), name="skill_graph_create"),
    path("skill-graph/<int:pk>/editar/", views.DependenciaFundamentoUpdateView.as_view(), name="skill_graph_update"),
    path("skill-graph/<int:pk>/excluir/", views.DependenciaFundamentoDeleteView.as_view(), name="skill_graph_delete"),


    path("materias_alunos/", views.materias_list_alunos, name="materias_list_alunos"),
    path("materia_alunos/<int:pk>/",views.materia_detail_alunos, name="materia_detail_alunos"),
    path("lista/materia/<int:pk>/", views.gerar_lista_materia_alunos, name="lista_materia_alunos"),
    path("lista/topico/<int:pk>/", views.gerar_lista_topico_alunos, name="lista_topico_alunos"),
    path("lista/fundamento/<int:pk>/", views.gerar_lista_fundamento_alunos, name="lista_fundamento_alunos"),

    path("importar-cronograma/", views.importar_cronograma, name="importar_cronograma"),
]