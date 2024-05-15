from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from .models import Professor,Disciplina, DiasSemana
from django.db import models 

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome','criado_em','modificado_em','ativo')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome','carga_horaria','criado_em','modificado_em','ativo')

@admin.register(DiasSemana)
class DiasSemanaAdmin(admin.ModelAdmin):
    list_display = ('dia','criado_em','modificado_em','ativo')
