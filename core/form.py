from django import forms
from .models import Disciplina

class DisciplinaForm(forms.Form):
    disciplinas = forms.ModelMultipleChoiceField(
        queryset=Disciplina.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )