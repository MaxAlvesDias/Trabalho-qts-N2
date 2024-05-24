from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from .models import Professor, Disciplina, DiasSemana, Horario, QTS, Disponibilidade, turma

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Disciplinas'] = Disciplina.objects.all()
        context['Professores'] = Professor.objects.all()
        context['DiasSemana'] = DiasSemana.objects.all()
        context['Horarios'] = Horario.objects.all()
        context['Disponibilidades'] = Disponibilidade.objects.all()
        context['Turmas'] = turma.objects.all()
        context['Periodos'] = Horario.objects.values('periodo').distinct()
        
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        quantidade = int(request.POST.get('quantidade', 0))
        qts_resultados = self.create_qts_matrices(quantidade)

        context = self.get_context_data()
        context['quantidade'] = quantidade
        context['qts_resultados'] = qts_resultados
        return render(request, self.template_name, context)
    
    def create_qts_matrices(self, quantidade):
        qts_matrices = {}

        for i in range(quantidade):
            qts_matriz = [
                ['', '', '', '', '', ''],
                ['', '', '', '', '', ''],
                ['', '', '', '', '', ''],
                ['', '', '', '', '', ''],
                ['', '', '', '', '', '']
            ]

            disciplinas = Disciplina.objects.all()
            professores = Professor.objects.all()

            for disciplina in disciplinas:
                for professor in professores:
                    disponibilidade = Disponibilidade.objects.filter(
                        professor=professor,
                        semana__dia= 'seg'
                    ).first()

                    if disponibilidade:
                        qts_criado = QTS.objects.filter(professor=professor).first()
                        

                        if not qts_criado:
                            qts = QTS.objects.create(
                                professor=professor,
                                disciplina=disciplina,
                                disponibilidade=disponibilidade
                            )

                            
                            qts_matriz[0][0] = "Horários"
                            qts_matriz[0][1] = get_object_or_404(DiasSemana, dia='seg')
                            qts_matriz[0][2] = get_object_or_404(DiasSemana, dia='ter')
                            qts_matriz[0][3] = get_object_or_404(DiasSemana, dia='qua')
                            qts_matriz[0][4] = get_object_or_404(DiasSemana, dia='qui')
                            qts_matriz[0][5] = get_object_or_404(DiasSemana, dia='sex')

                            qts_matriz[1][0] = get_object_or_404(Horario, periodo='1º Período')
                            qts_matriz[2][0] = get_object_or_404(Horario, periodo='2º Período')
                            qts_matriz[3][0] = get_object_or_404(Horario, periodo='3º Período')
                            qts_matriz[4][0] = get_object_or_404(Horario, periodo='4º Período')

                            if disciplina.carga_horaria == 80:
                                qts_matriz[1][1] = qts
                                qts_matriz[2][1] = qts
                                qts_matriz[3][1] = qts
                                qts_matriz[4][1] = qts
                                break
                            elif disciplina.carga_horaria == 60:
                                qts_matriz[1][1] = qts
                                qts_matriz[2][1] = qts
                                qts_matriz[3][1] = qts
                                qts_matriz[4][1] = '-'
                                break
                            elif disciplina.carga_horaria == 40:
                                qts_matriz[1][1] = qts
                                qts_matriz[2][1] = qts

                                for disciplina in disciplinas:
                                    for professor in professores:
                                        disponibilidade = Disponibilidade.objects.filter(
                                            professor=professor,
                                            semana__dia='seg'
                                        ).first()
                                        if disponibilidade:
                                            qts_criado = QTS.objects.filter(
                                                professor=professor,
                                                disciplina = disciplina
                                            ).first()
                                            
                                            if not qts_criado:
                                                qts = QTS.objects.create(
                                                    professor=professor,
                                                    disciplina=disciplina,
                                                    disponibilidade=disponibilidade
                                                )

                                                if disciplina.carga_horaria == 40:
                                                    qts_matriz[3][1] = qts
                                                    qts_matriz[4][1] = qts
                                                    break
                
            qts_matrices[i] = qts_matriz
    
        return qts_matrices
