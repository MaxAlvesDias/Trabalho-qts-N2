from django.views.generic import TemplateView
from .models import Professor, Disciplina, DiasSemana, Horario

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['Disciplina'] = Disciplina.objects.all()
        context['Professor'] = Professor.objects.all()
        context['DiasSemana'] = DiasSemana.objects.all()
        context['dias_semana'] = DiasSemana.objects.all()
        context['Horarios'] = Horario.objects.all()
        context['Periodo'] = Horario.objects.values('periodo').distinct()

        return context
