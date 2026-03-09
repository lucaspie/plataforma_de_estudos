from django import forms
from django.forms import inlineformset_factory

from .models import Concurso, Materia, Topico, Fundamento, Questao, Opcao


class ConcursoForm(forms.ModelForm):
    class Meta:
        model = Concurso
        fields = "__all__"


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = "__all__"


class TopicoForm(forms.ModelForm):
    class Meta:
        model = Topico
        fields = "__all__"


class FundamentoForm(forms.ModelForm):
    class Meta:
        model = Fundamento
        fields = "__all__"


class QuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        fields = [
            "concurso",
            "topico",
            "fundamentos",
            "texto",
            "imagem",
            "origem",
            "ano",
            "nivel_sugerido",
            "resolucao_mestra",
        ]


OpcaoFormSet = inlineformset_factory(
    Questao,
    Opcao,
    fields=("texto", "correta", "comentario"),
    extra=5,
    can_delete=True
)

class OpcaoForm(forms.ModelForm):
    class Meta:
        model = Opcao
        fields = "__all__"