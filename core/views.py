from django.views.generic import TemplateView
from .models import Professor, Disciplina, DiasSemana

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['Disciplina'] = Disciplina.objects.all()
        context['Professor'] = Professor.objects.all()
        context['DiasSemana'] = DiasSemana.objects.all()
        context['dias_semana'] = DiasSemana.objects.values_list('dia', flat=True).distinct()

        # Recuperando os horários de início e fim de cada dia da semana do banco de dados
        horarios_inicio = set()
        horarios_fim = set()
        for dia in DiasSemana.objects.all():
            horarios_inicio.add(dia.horario_1_inicio)
            horarios_inicio.add(dia.horario_2_inicio)
            horarios_inicio.add(dia.horario_3_inicio)
            horarios_inicio.add(dia.horario_4_inicio)
            horarios_fim.add(dia.horario_1_fim)
            horarios_fim.add(dia.horario_2_fim)
            horarios_fim.add(dia.horario_3_fim)
            horarios_fim.add(dia.horario_4_fim)

        # Remover horários None (sem horário definido)
        horarios_inicio.discard(None)
        horarios_fim.discard(None)

        # Agrupar horários em pares
        horarios_pares = list(zip(sorted(horarios_inicio), sorted(horarios_fim)))
        
        context['horarios'] = horarios_pares        
        return context
