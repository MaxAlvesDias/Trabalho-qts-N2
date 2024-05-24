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
        qts_segunda = None
        qts_terca = None
        qts_quarta = None
        qts_quinta = None
        qts_sexta = None


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

                    #QTS para o dias de segunda-feira
                    disponibilidade_segunda = Disponibilidade.objects.filter(
                        professor=professor,
                        semana__dia= 'seg'
                    ).first()

                    if disponibilidade_segunda:
                        qts_criado_segunda = QTS.objects.filter(
                            professor=professor,
                            disciplina = disciplina,
                            disponibilidade = disponibilidade_segunda
                            ).first()
                        

                        if not qts_criado_segunda:
                            qts_segunda = QTS.objects.create(
                                professor=professor,
                                disciplina=disciplina,
                                disponibilidade = disponibilidade_segunda
                            )
                        
                        else:
                            qts_segunda = qts_criado_segunda

                            
                        
                        
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
                            qts_matriz[1][1] = qts_segunda
                            qts_matriz[2][1] = qts_segunda
                            qts_matriz[3][1] = qts_segunda
                            qts_matriz[4][1] = qts_segunda
                            
                        elif disciplina.carga_horaria == 60:
                            qts_matriz[1][1] = qts_segunda
                            qts_matriz[2][1] = qts_segunda
                            qts_matriz[3][1] = qts_segunda
                            qts_matriz[4][1] = '-'
                            
                        elif disciplina.carga_horaria == 40:
                            qts_matriz[1][1] = qts_segunda
                            qts_matriz[2][1] = qts_segunda

                            for disciplina in disciplinas:
                                for professor in professores:
                                    disponibilidade = Disponibilidade.objects.filter(
                                        professor= professor,
                                        semana__dia='seg'
                                    ).first()

                                    if disponibilidade:
                                        qts_criado_segunda = QTS.objects.filter(
                                            professor= professor,
                                            disciplina = disciplina,
                                            disponibilidade = disponibilidade
                                        ).first()
                                            
                                        if not qts_criado_segunda:
                                            qts_segunda = QTS.objects.create(
                                                professor=professor,
                                                disciplina=disciplina,
                                                disponibilidade=disponibilidade
                                            )
                                        if qts_criado_segunda:
                                            qts_segunda = qts_criado_segunda

                                            if disciplina.carga_horaria == 40:
                                                qts_matriz[3][1] = qts_segunda
                                                qts_matriz[4][1] = qts_segunda

            for disciplina_terca in disciplinas:
                for professor_terca in professores:

                    disponibilidade_terca = Disponibilidade.objects.filter(
                        professor=professor_terca,
                        semana__dia= 'ter'
                    ).first()                

                    if disponibilidade_terca:
                        qts_criado_terca = QTS.objects.filter(
                            professor=professor_terca,
                            disciplina = disciplina_terca,
                            disponibilidade = disponibilidade_terca
                            ).first()
                        
                                                

                        if not qts_criado_terca:
                            qts_terca = QTS.objects.create(
                                professor=professor_terca,
                                disciplina=disciplina_terca,
                                disponibilidade=disponibilidade_terca
                            )
                        
                        else:
                            qts_terca = qts_criado_terca


                        if disciplina.carga_horaria == 80 and qts_segunda.disciplina != qts_terca.disciplina:
                            qts_matriz[1][2] = qts_terca
                            qts_matriz[2][2] = qts_terca
                            qts_matriz[3][2] = qts_terca
                            qts_matriz[4][2] = qts_terca
                            
                        elif disciplina.carga_horaria == 60 and qts_segunda.disciplina != qts_terca.disciplina:
                            qts_matriz[1][2] = qts_terca
                            qts_matriz[2][2] = qts_terca
                            qts_matriz[3][2] = qts_terca
                            qts_matriz[4][2] = '-'
                            
                        elif disciplina.carga_horaria == 40 and qts_segunda.disciplina != qts_terca.disciplina:
                            qts_matriz[1][2] = qts_terca
                            qts_matriz[2][2] = qts_terca

                            for disciplina in disciplinas:
                                for professor in professores:
                                    disponibilidade_terca = Disponibilidade.objects.filter(
                                        professor= professor,
                                        semana__dia='ter'
                                    ).first()

                                    if disponibilidade_terca:
                                        qts_criado_terca = QTS.objects.filter(
                                            professor= professor,
                                            disciplina = disciplina,
                                            disponibilidade = disponibilidade_terca
                                        ).first()
                                            
                                        if not qts_criado_terca:
                                            qts_terca = QTS.objects.create(
                                                professor=professor_terca,
                                                disciplina=disciplina_terca,
                                                disponibilidade=disponibilidade_terca
                                            )
                                        if qts_criado_terca:
                                            qts_terca = qts_criado_terca

                                            if disciplina.carga_horaria == 40 and qts_segunda.disciplina != qts_terca.disciplina:
                                                qts_matriz[3][2] = qts_terca
                                                qts_matriz[4][2] = qts_terca 

                                            
                
            qts_matrices[i] = qts_matriz
    
        return qts_matrices
