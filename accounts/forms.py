from django.contrib.auth.forms import UserCreationForm
from django import forms

from accounts.models import Usuario

class CadastroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["username", "nome_completo", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo = "aluno"
        if commit:
            user.save()
        return user


class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nome_completo", "email", "tipo", "is_active"]