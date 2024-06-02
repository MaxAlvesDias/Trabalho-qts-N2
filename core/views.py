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
        context['QTS'] = QTS.objects.all()
        context['Turmas'] = turma.objects.all()
        context['Periodos'] = Horario.objects.values('periodo').distinct()
        
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        quantidade = int(request.POST.get('quantidade', 0))
        qts_resultados = self.create_qts_matrices()
        montar_matriz = self.montar_qts(quantidade)
        context = self.get_context_data()
        context['quantidade'] = quantidade
        context['qts_resultados'] = qts_resultados
        context['montar_matriz'] = montar_matriz

        return render(request, self.template_name, context) 
    
    def create_qts_matrices(self):

        disciplinas = Disciplina.objects.all()
        professores = Professor.objects.all()
            
# criar todos os possibilidades de Segunda-feira
        for disciplina in disciplinas:
            for professor in professores:

                apto_segunda = Disciplina.objects.filter(
                    Professor = professor,
                    nome=disciplina.nome
                ).exists()

                disponibilidade_segunda = Disponibilidade.objects.filter(
                    professor=professor,
                    semana__dia= 'seg',
                ).first()

                if disponibilidade_segunda and apto_segunda:
                    qts_criado_segunda = QTS.objects.filter(
                        professor=professor,
                        disciplina = disciplina,
                        disponibilidade = disponibilidade_segunda,
                        ).first()                        

                    if not qts_criado_segunda:
                        qts_segunda = QTS.objects.create(
                            professor=professor,
                            disciplina=disciplina,
                            disponibilidade = disponibilidade_segunda
                        )
                        
                    else:
                        qts_segunda = qts_criado_segunda

            # criar todos os possibilidades de terça feira
        for disciplina_terca in disciplinas:
            for professor_terca in professores:
                apto = Disciplina.objects.filter(
                    Professor = professor_terca,
                    nome=disciplina_terca.nome
                ).exists()

                disponibilidade_terca = Disponibilidade.objects.filter(
                    professor=professor_terca,
                    semana__dia= 'ter'
                ).first()                

                if disponibilidade_terca and apto:
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

            # criar todos os possibilidades de quarta-feira

        for disciplina_quarta in disciplinas:
            for professor_quarta in professores:

                apt_quarta = Disciplina.objects.filter(
                    Professor = professor_quarta,
                    nome = disciplina_quarta.nome
                ).exists()

                disponibilidade_quarta = Disponibilidade.objects.filter(
                    professor=professor_quarta,
                    semana__dia= 'qua'
                ).first()                

                if disponibilidade_quarta and apt_quarta:
                    qts_criado_quarta = QTS.objects.filter(
                        professor=professor_quarta,
                        disciplina = disciplina_quarta,
                        disponibilidade = disponibilidade_quarta
                        ).first()                                                

                    if not qts_criado_quarta:
                        qts_quarta = QTS.objects.create(
                            professor=professor_quarta,
                            disciplina=disciplina_quarta,
                            disponibilidade=disponibilidade_quarta
                        )
                        
                    else:
                        qts_quarta = qts_criado_quarta
                          
            # criar todos os possibilidades de quinta-feira

        for disciplina_quinta in disciplinas:
            for professor_quinta in professores:

                apt_quinta = Disciplina.objects.filter(
                    Professor = professor_quinta,
                    nome = disciplina_quinta.nome
                ).exists()

                disponibilidade_quinta = Disponibilidade.objects.filter(
                    professor=professor_quinta,
                    semana__dia= 'qui'
                ).first()                

                if disponibilidade_quinta and apt_quinta:
                    qts_criado_quinta = QTS.objects.filter(
                        professor=professor_quinta,
                        disciplina = disciplina_quinta,
                        disponibilidade = disponibilidade_quinta
                        ).first()
                        
                                                

                    if not qts_criado_quinta:
                        qts_quinta = QTS.objects.create(
                            professor=professor_quinta,
                            disciplina=disciplina_quinta,
                            disponibilidade=disponibilidade_quinta
                        )
                        
                    else:
                        qts_quinta = qts_criado_quinta
                                
            # criar todos os possibilidades de sexta-feira

        for disciplina_sexta in disciplinas:
            for professor_sexta in professores:

                apt_sexta = Disciplina.objects.filter(
                    Professor = professor_sexta,
                    nome = disciplina_sexta.nome
                ).exists()

                disponibilidade_sexta = Disponibilidade.objects.filter(
                    professor=professor_sexta,
                    semana__dia= 'sex'
                ).first()                

                if disponibilidade_sexta and apt_sexta:
                    qts_criado_sexta = QTS.objects.filter(
                        professor=professor_sexta,
                        disciplina = disciplina_sexta,
                        disponibilidade = disponibilidade_sexta
                        ).first()
                        
                                                

                    if not qts_criado_sexta:
                        qts_sexta = QTS.objects.create(
                            professor=professor_sexta,
                            disciplina=disciplina_sexta,
                            disponibilidade=disponibilidade_sexta
                        )
                        
                    else:
                        qts_sexta = qts_criado_sexta

    
        return {
            'qts_segunda': qts_segunda,
            'qts_terca': qts_terca,
            'qts_quarta': qts_quarta,
            'qts_quinta': qts_quinta,
            'qts_sexta': qts_sexta,
        }
    

            #função para criar os QTS e as funções de controle de materia e professor
    def montar_qts(self, quantidade):
        qts_matrices = {}
        qts = QTS.objects.all()

        dias_semana = ['seg', 'ter', 'qua', 'qui', 'sex']
        professores_usados = {dia: set() for dia in dias_semana}
        disciplinas_usadas = set()

        for i in range(quantidade):
            qts_matriz = [
                ['', '', '', '', '', ''],
                ['', '', '', '', '', ''],
                ['', '', '', '', '', ''],
                ['', '', '', '', '', ''],
                ['', '', '', '', '', '']
            ]

            qts_matriz[0][0] = "Horários"
            for index, dia in enumerate(dias_semana, start=1):
                qts_matriz[0][index] = get_object_or_404(DiasSemana, dia=dia)

            qts_matriz[1][0] = get_object_or_404(Horario, periodo='1º Período')
            qts_matriz[2][0] = get_object_or_404(Horario, periodo='2º Período')
            qts_matriz[3][0] = get_object_or_404(Horario, periodo='3º Período')
            qts_matriz[4][0] = get_object_or_404(Horario, periodo='4º Período')

            for dia in dias_semana:
                for qts_resultados in qts:
                    disponibilidade = Disponibilidade.objects.filter(
                        semana__dia=dia,
                        professor=qts_resultados.professor
                    ).first()

                    if disponibilidade:
                        if (qts_resultados.disciplina.carga_horaria == 80 and
                            qts_resultados.professor not in professores_usados[dia] and
                            qts_resultados.disciplina not in disciplinas_usadas):
                            professores_usados[dia].add(qts_resultados.professor)
                            disciplinas_usadas.add(qts_resultados.disciplina)
                            qts_matriz[1][dias_semana.index(dia) + 1] = qts_resultados
                            qts_matriz[2][dias_semana.index(dia) + 1] = qts_resultados
                            qts_matriz[3][dias_semana.index(dia) + 1] = qts_resultados
                            qts_matriz[4][dias_semana.index(dia) + 1] = qts_resultados
                            break

                        elif (qts_resultados.disciplina.carga_horaria == 60 and
                              qts_resultados.professor not in professores_usados[dia] and
                              qts_resultados.disciplina not in disciplinas_usadas):
                            professores_usados[dia].add(qts_resultados.professor)
                            disciplinas_usadas.add(qts_resultados.disciplina)
                            qts_matriz[1][dias_semana.index(dia) + 1] = qts_resultados
                            qts_matriz[2][dias_semana.index(dia) + 1] = qts_resultados
                            qts_matriz[3][dias_semana.index(dia) + 1] = qts_resultados
                            qts_matriz[4][dias_semana.index(dia) + 1] = '-'
                            break

                        elif (qts_resultados.disciplina.carga_horaria == 40 and
                              qts_resultados.professor not in professores_usados[dia] and
                              qts_resultados.disciplina not in disciplinas_usadas):
                            professores_usados[dia].add(qts_resultados.professor)
                            disciplinas_usadas.add(qts_resultados.disciplina)
                            qts_matriz[1][dias_semana.index(dia) + 1] = qts_resultados
                            qts_matriz[2][dias_semana.index(dia) + 1] = qts_resultados

                            for qts_resultados2 in qts:
                                disponibilidade2 = Disponibilidade.objects.filter(
                                    semana__dia=dia,
                                    professor=qts_resultados2.professor
                                ).first()

                                if disponibilidade2:
                                    if (qts_resultados2.disciplina.carga_horaria == 40 and
                                        qts_resultados2.disciplina not in disciplinas_usadas and
                                        qts_resultados2.professor in professores_usados[dia] and
                                        qts_resultados.professor == qts_resultados2.professor):
                                        disciplinas_usadas.add(qts_resultados2.disciplina)
                                        qts_matriz[3][dias_semana.index(dia) + 1] = qts_resultados2
                                        qts_matriz[4][dias_semana.index(dia) + 1] = qts_resultados2
                                        break

                                    elif (qts_resultados2.disciplina.carga_horaria == 40 and
                                          qts_resultados2.disciplina not in disciplinas_usadas and
                                          qts_resultados2.professor not in professores_usados[dia]):
                                        disciplinas_usadas.add(qts_resultados2.disciplina)
                                        professores_usados[dia].add(qts_resultados2.professor)
                                        qts_matriz[3][dias_semana.index(dia) + 1] = qts_resultados2
                                        qts_matriz[4][dias_semana.index(dia) + 1] = qts_resultados2
                                        break
                            break

            qts_matrices[i] = qts_matriz

        return qts_matrices
    
class QtsView(TemplateView):
    template_name = 'qts.html'

    def post(self, request, *args, **kwargs):
        quantidade = int(request.POST.get('quantidade', 0))
        context = self.get_context_data()
        context['quantidade'] = quantidade
        context['qts_resultados'] = IndexView.create_qts_matrices(self)
        context['montar_matriz'] = IndexView.montar_qts(self, quantidade)

        return render(request, self.template_name, context)
    


