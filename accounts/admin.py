from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ("Informações adicionais", {
            "fields": ("nome_completo", "tipo")
        }),
    )

    list_display = ("username", "email", "tipo", "is_staff", "is_active")