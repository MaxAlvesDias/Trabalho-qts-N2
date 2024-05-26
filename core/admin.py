from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from .models import Professor, Disciplina, DiasSemana, Horario, Disponibilidade, QTS
from django.db import models 

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em', 'modificado_em', 'ativo')

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'carga_horaria', 'criado_em', 'modificado_em', 'ativo')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

@admin.register(DiasSemana)
class DiasSemanaAdmin(admin.ModelAdmin):
    list_display = ('dia', 'criado_em', 'modificado_em', 'ativo')

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('periodo', 'criado_em', 'modificado_em', 'ativo')


@admin.register(Disponibilidade)
class DisponibilidadeAdmin(admin.ModelAdmin):
    list_display = ('get_professores', 'criado_em', 'modificado_em', 'ativo')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def get_professores(self, obj):
        return obj.get_professores()
    get_professores.short_description = 'Professores'

@admin.register(QTS)
class QtsAdmin(admin.ModelAdmin):
    list_display = ('criado_em', 'modificado_em', 'ativo')


