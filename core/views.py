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

        professores_usados_segunda = set()
        professores_usados_terca = set()
        professores_usados_quarta = set()
        professores_usados_quinta = set()
        professores_usados_sexta = set()
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
            qts_matriz[0][1] = get_object_or_404(DiasSemana, dia='seg')
            qts_matriz[0][2] = get_object_or_404(DiasSemana, dia='ter')
            qts_matriz[0][3] = get_object_or_404(DiasSemana, dia='qua')
            qts_matriz[0][4] = get_object_or_404(DiasSemana, dia='qui')
            qts_matriz[0][5] = get_object_or_404(DiasSemana, dia='sex')
 
            qts_matriz[1][0] = get_object_or_404(Horario, periodo='1º Período')
            qts_matriz[2][0] = get_object_or_404(Horario, periodo='2º Período')
            qts_matriz[3][0] = get_object_or_404(Horario, periodo='3º Período')
            qts_matriz[4][0] = get_object_or_404(Horario, periodo='4º Período')

        # Segunda-feira

            for qts_resultados_segunda in qts:
                                               
                disponibilidade_segunda = Disponibilidade.objects.filter(
                    semana__dia= 'seg',
                    professor = qts_resultados_segunda.professor
                ).first()

                if disponibilidade_segunda:
                    if (qts_resultados_segunda.disciplina.carga_horaria == 80 and
                    qts_resultados_segunda.professor not in professores_usados_segunda and
                    qts_resultados_segunda.disciplina not in disciplinas_usadas):
                        professores_usados_segunda.add(qts_resultados_segunda.professor)
                        disciplinas_usadas.add(qts_resultados_segunda.disciplina)
                        qts_matriz[1][1] = qts_resultados_segunda
                        qts_matriz[2][1] = qts_resultados_segunda
                        qts_matriz[3][1] = qts_resultados_segunda
                        qts_matriz[4][1] = qts_resultados_segunda

                        break

                    elif (qts_resultados_segunda.disciplina.carga_horaria == 60 and
                    qts_resultados_segunda.professor not in professores_usados_segunda and
                    qts_resultados_segunda.disciplina not in disciplinas_usadas):
                        professores_usados_segunda.add(qts_resultados_segunda.professor)
                        disciplinas_usadas.add(qts_resultados_segunda.disciplina)
                        qts_matriz[1][1] = qts_resultados_segunda
                        qts_matriz[2][1] = qts_resultados_segunda
                        qts_matriz[3][1] = qts_resultados_segunda
                        qts_matriz[4][1] = '-'

                        break
                             
                    elif (qts_resultados_segunda.disciplina.carga_horaria == 40 and
                    qts_resultados_segunda.professor not in professores_usados_segunda and
                    qts_resultados_segunda.disciplina not in disciplinas_usadas):
                        professores_usados_segunda.add(qts_resultados_segunda.professor)
                        disciplinas_usadas.add(qts_resultados_segunda.disciplina)
                        qts_matriz[1][1] = qts_resultados_segunda
                        qts_matriz[2][1] = qts_resultados_segunda
 
                        for qts_resultados_segunda2 in qts:

                            disponibilidade_segunda2 = Disponibilidade.objects.filter(
                                semana__dia = 'seg',
                                professor = qts_resultados_segunda2.professor
                            )

                            if disponibilidade_segunda2:

                                if (qts_resultados_segunda2.disciplina.carga_horaria == 40 and
                                qts_resultados_segunda2.disciplina not in disciplinas_usadas and
                                qts_resultados_segunda2.professor in professores_usados_segunda):
                                    disciplinas_usadas.add(qts_resultados_segunda2.disciplina)
                                    qts_matriz[3][1] = qts_resultados_segunda2
                                    qts_matriz[4][1] = qts_resultados_segunda2

                                    break
                    
                                elif (qts_resultados_segunda2.disciplina.carga_horaria == 40 and
                                qts_resultados_segunda2.disciplina not in disciplinas_usadas and
                                qts_resultados_segunda2.professor not in professores_usados_segunda):
                                    disciplinas_usadas.add(qts_resultados_segunda2.disciplina)
                                    professores_usados_segunda.add(qts_resultados_segunda2.professor)
                                    qts_matriz[3][1] = qts_resultados_segunda2
                                    qts_matriz[4][1] = qts_resultados_segunda2

                                    break

                        break                
        # Terça-feira

            for qts_resultados_terca in qts:
                                               
                disponibilidade_terca = Disponibilidade.objects.filter(
                    semana__dia= 'ter',
                    professor = qts_resultados_terca.professor
                ).first()

                if disponibilidade_terca:
                    if (qts_resultados_terca.disciplina.carga_horaria == 80 and
                    qts_resultados_terca.professor not in professores_usados_terca and
                    qts_resultados_terca.disciplina not in disciplinas_usadas):
                        disciplinas_usadas.add(qts_resultados_terca.disciplina)
                        professores_usados_terca.add(qts_resultados_terca.professor)
                        qts_matriz[1][2] = qts_resultados_terca
                        qts_matriz[2][2] = qts_resultados_terca
                        qts_matriz[3][2] = qts_resultados_terca
                        qts_matriz[4][2] = qts_resultados_terca


                        break

                    elif (qts_resultados_terca.disciplina.carga_horaria == 60 and
                    qts_resultados_terca.professor not in professores_usados_terca and
                    qts_resultados_terca.disciplina not in disciplinas_usadas):
                        disciplinas_usadas.add(qts_resultados_terca.disciplina)
                        professores_usados_terca.add(qts_resultados_terca.professor)
                        qts_matriz[1][2] = qts_resultados_terca
                        qts_matriz[2][2] = qts_resultados_terca
                        qts_matriz[3][2] = qts_resultados_terca
                        qts_matriz[4][2] = '-'

                        break
                             
                    elif (qts_resultados_terca.disciplina.carga_horaria == 40 and
                    qts_resultados_terca.professor not in professores_usados_terca and
                    qts_resultados_terca.disciplina not in disciplinas_usadas):
                        disciplinas_usadas.add(qts_resultados_terca.disciplina)  
                        professores_usados_terca.add(qts_resultados_terca.professor)
                        qts_matriz[1][2] = qts_resultados_terca
                        qts_matriz[2][2] = qts_resultados_terca
                            
                        for qts_resultados_terca2 in qts:

                            disponibilidade_terca2 = Disponibilidade.objects.filter(
                                semana__dia = 'ter',
                                professor = qts_resultados_terca2.professor
                            )

                            if disponibilidade_terca2:

                                if (qts_resultados_terca2.disciplina.carga_horaria == 40 and
                                qts_resultados_terca2.disciplina not in disciplinas_usadas and
                                qts_resultados_terca2.professor in professores_usados_terca):
                                    disciplinas_usadas.add(qts_resultados_terca2.disciplina)
                                    qts_matriz[3][2] = qts_resultados_terca2
                                    qts_matriz[4][2] = qts_resultados_terca2

                                    break

                                elif (qts_resultados_terca2.disciplina.carga_horaria == 40 and
                                qts_resultados_terca2.disciplina not in disciplinas_usadas and
                                qts_resultados_terca2.professor not in professores_usados_terca):
                                    disciplinas_usadas.add(qts_resultados_terca2.disciplina)
                                    professores_usados_terca.add(qts_resultados_terca2.professor)
                                    qts_matriz[3][2] = qts_resultados_terca2
                                    qts_matriz[4][2] = qts_resultados_terca2

                                    break

                        break        

        # Quarta-feira

            for qts_resultados_quarta in qts:
                                               
                disponibilidade_quarta = Disponibilidade.objects.filter(
                    semana__dia= 'qua',
                    professor = qts_resultados_quarta.professor
                ).first()

                if disponibilidade_quarta:
                    if (qts_resultados_quarta.disciplina.carga_horaria == 80 and
                    qts_resultados_quarta.professor not in professores_usados_quarta and
                    qts_resultados_quarta.disciplina not in disciplinas_usadas):
                        disciplinas_usadas.add(qts_resultados_quarta.disciplina)
                        professores_usados_quarta.add(qts_resultados_quarta.professor)
                        qts_matriz[1][3] = qts_resultados_quarta
                        qts_matriz[2][3] = qts_resultados_quarta
                        qts_matriz[3][3] = qts_resultados_quarta
                        qts_matriz[4][3] = qts_resultados_quarta

                        break

                    elif (qts_resultados_quarta.disciplina.carga_horaria == 60 and
                    qts_resultados_quarta.professor not in professores_usados_quarta and
                    qts_resultados_quarta.disciplina not in disciplinas_usadas):
                        disciplinas_usadas.add(qts_resultados_quarta.disciplina)
                        professores_usados_quarta.add(qts_resultados_quarta.professor)
                        qts_matriz[1][3] = qts_resultados_quarta
                        qts_matriz[2][3] = qts_resultados_quarta
                        qts_matriz[3][3] = qts_resultados_quarta
                        qts_matriz[4][3] = '-'

                        break
                             
                    elif (qts_resultados_quarta.disciplina.carga_horaria == 40 and
                    qts_resultados_quarta.professor not in professores_usados_quarta and
                    qts_resultados_quarta.disciplina not in disciplinas_usadas):
                        disciplinas_usadas.add(qts_resultados_quarta.disciplina)  
                        professores_usados_quarta.add(qts_resultados_quarta.professor)
                        qts_matriz[1][3] = qts_resultados_quarta
                        qts_matriz[2][3] = qts_resultados_quarta

                            
                        for qts_resultados_quarta2 in qts:

                            disponibilidade_quarta2 = Disponibilidade.objects.filter(
                                semana__dia = 'qua',
                                professor = qts_resultados_quarta2.professor
                            )
                                
                            if disponibilidade_quarta2:

                                if (qts_resultados_quarta2.disciplina.carga_horaria == 40 and
                                qts_resultados_quarta2.disciplina not in disciplinas_usadas and
                                qts_resultados_quarta2.professor in professores_usados_quarta):
                                    disciplinas_usadas.add(qts_resultados_quarta2.disciplina)
                                    qts_matriz[3][3] = qts_resultados_quarta2
                                    qts_matriz[4][3] = qts_resultados_quarta2

                                    break             

                                elif (qts_resultados_quarta2.disciplina.carga_horaria == 40 and
                                qts_resultados_quarta2.disciplina not in disciplinas_usadas and
                                qts_resultados_quarta2.professor not in professores_usados_quarta):
                                    disciplinas_usadas.add(qts_resultados_quarta2.disciplina)
                                    professores_usados_quarta.add(qts_resultados_quarta2.professor)
                                    qts_matriz[3][3] = qts_resultados_quarta2
                                    qts_matriz[4][3] = qts_resultados_quarta2

                                    break

                        break

        # Quinta-feira

            for qts_resultados_quinta in qts:
                                               
                disponibilidade_quinta = Disponibilidade.objects.filter(
                    semana__dia= 'qui',
                    professor = qts_resultados_quinta.professor
                ).first()

                if disponibilidade_quinta:
                    if (qts_resultados_quinta.disciplina.carga_horaria == 80 and
                    qts_resultados_quinta.professor not in professores_usados_quinta and
                    qts_resultados_quinta.disciplina not in disciplinas_usadas):
                        disciplinas_usadas.add(qts_resultados_quinta.disciplina)
                        professores_usados_quinta.add(qts_resultados_quinta.professor)
                        qts_matriz[1][4] = qts_resultados_quinta
                        qts_matriz[2][4] = qts_resultados_quinta
                        qts_matriz[3][4] = qts_resultados_quinta
                        qts_matriz[4][4] = qts_resultados_quinta


                        break

                    elif (qts_resultados_quinta.disciplina.carga_horaria == 60 and
                    qts_resultados_quinta.professor not in professores_usados_quinta and
                    qts_resultados_quinta.disciplina not in disciplinas_usadas):
                        disciplinas_usadas.add(qts_resultados_quinta.disciplina)
                        professores_usados_quinta.add(qts_resultados_quinta.professor)
                        qts_matriz[1][4] = qts_resultados_quinta
                        qts_matriz[2][4] = qts_resultados_quinta
                        qts_matriz[3][4] = qts_resultados_quinta
                        qts_matriz[4][4] = '-'

                        break
                             
                    elif (qts_resultados_quinta.disciplina.carga_horaria == 40 and
                    qts_resultados_quinta.professor not in professores_usados_quinta and
                    qts_resultados_quinta.disciplina not in disciplinas_usadas):
                        disciplinas_usadas.add(qts_resultados_quinta.disciplina)  
                        professores_usados_quinta.add(qts_resultados_quinta.professor)
                        qts_matriz[1][4] = qts_resultados_quinta
                        qts_matriz[2][4] = qts_resultados_quinta

                            
                        for qts_resultados_quinta2 in qts:

                            disponibilidade_quinta2 = Disponibilidade.objects.filter(
                                semana__dia = 'qui',
                                professor = qts_resultados_quinta2.professor
                            )

                            if disponibilidade_quinta2:

                                if (qts_resultados_quinta2.disciplina.carga_horaria == 40 and
                                qts_resultados_quinta2.disciplina not in disciplinas_usadas and
                                qts_resultados_quinta2.professor in professores_usados_quinta):
                                    disciplinas_usadas.add(qts_resultados_quinta2.disciplina)
                                    qts_matriz[3][4] = qts_resultados_quinta2
                                    qts_matriz[4][4] = qts_resultados_quinta2

                                    break

                                elif (qts_resultados_quinta2.disciplina.carga_horaria == 40 and
                                qts_resultados_quinta2.disciplina not in disciplinas_usadas and
                                qts_resultados_quinta2.professor not in professores_usados_quinta):
                                    disciplinas_usadas.add(qts_resultados_quinta2.disciplina)
                                    professores_usados_quinta.add(qts_resultados_quinta2.professor)
                                    qts_matriz[3][4] = qts_resultados_quinta2
                                    qts_matriz[4][4] = qts_resultados_quinta2

                                    break

                        break

        # sexta-feira

            for qts_resultados_sexta in qts:
                                               
                disponibilidade_sexta = Disponibilidade.objects.filter(
                    semana__dia= 'sex',
                    professor = qts_resultados_sexta.professor
                ).first()

                if disponibilidade_sexta:
                    if (qts_resultados_sexta.disciplina.carga_horaria == 80 and
                    qts_resultados_sexta.professor not in professores_usados_sexta and
                    qts_resultados_sexta.disciplina not in disciplinas_usadas):
                        disciplinas_usadas.add(qts_resultados_sexta.disciplina)
                        professores_usados_sexta.add(qts_resultados_sexta.professor)
                        qts_matriz[1][5] = qts_resultados_sexta
                        qts_matriz[2][5] = qts_resultados_sexta
                        qts_matriz[3][5] = qts_resultados_sexta
                        qts_matriz[4][5] = qts_resultados_sexta

                        break

                    elif (qts_resultados_sexta.disciplina.carga_horaria == 60 and
                    qts_resultados_sexta.professor not in professores_usados_sexta and
                    qts_resultados_sexta.disciplina not in disciplinas_usadas):
                        disciplinas_usadas.add(qts_resultados_sexta.disciplina)
                        professores_usados_sexta.add(qts_resultados_sexta.professor)
                        qts_matriz[1][5] = qts_resultados_sexta
                        qts_matriz[2][5] = qts_resultados_sexta
                        qts_matriz[3][5] = qts_resultados_sexta
                        qts_matriz[4][5] = '-'

                        break
                             
                    elif (qts_resultados_sexta.disciplina.carga_horaria == 40 and
                    qts_resultados_sexta.professor not in professores_usados_sexta and
                    qts_resultados_sexta.disciplina not in disciplinas_usadas):
                            disciplinas_usadas.add(qts_resultados_sexta.disciplina)  
                            professores_usados_sexta.add(qts_resultados_sexta.professor)
                            qts_matriz[1][5] = qts_resultados_sexta
                            qts_matriz[2][5] = qts_resultados_sexta

                            
                            for qts_resultados_sexta2 in qts:

                                disponibilidade_sexta2 = Disponibilidade.objects.filter(
                                    semana__dia = 'sex',
                                    professor = qts_resultados_sexta2.professor
                                )

                                if disponibilidade_sexta2:

                                    if (qts_resultados_sexta2.disciplina.carga_horaria == 40 and
                                    qts_resultados_sexta2.disciplina not in disciplinas_usadas and
                                    qts_resultados_sexta2.professor in professores_usados_sexta):
                                        disciplinas_usadas.add(qts_resultados_sexta2.disciplina)
                                        qts_matriz[3][5] = qts_resultados_sexta2
                                        qts_matriz[4][5] = qts_resultados_sexta2

                                        break

                                    elif (qts_resultados_sexta2.disciplina.carga_horaria == 40 and
                                    qts_resultados_sexta2.disciplina not in disciplinas_usadas and
                                    qts_resultados_sexta2.professor not in professores_usados_sexta):
                                        disciplinas_usadas.add(qts_resultados_sexta2.disciplina)
                                        professores_usados_sexta.add(qts_resultados_sexta2.professor)
                                        qts_matriz[3][5] = qts_resultados_sexta2
                                        qts_matriz[4][5] = qts_resultados_sexta2

                                        break

                            break

            qts_matrices[i] = qts_matriz

        return qts_matrices 
