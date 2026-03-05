from django.urls import path
from . import views

urlpatterns = [
    path("cadastro/", views.cadastro, name="cadastro"),
    path("redirect/", views.redirect_after_login, name="redirect_after_login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    path("usuarios/<int:pk>/editar/", views.editar_usuario, name="editar_usuario"),
    path("usuarios/<int:pk>/toggle/", views.toggle_usuario, name="toggle_usuario"),
    path("cadastro/", views.cadastro, name="cadastro"),
]