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

            
# Segunda-feira
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

                        if qts_segunda.disciplina.carga_horaria == 80:
                            qts_matriz[1][1] = qts_segunda
                            qts_matriz[2][1] = qts_segunda
                            qts_matriz[3][1] = qts_segunda
                            qts_matriz[4][1] = qts_segunda
                            
                        elif qts_segunda.disciplina.carga_horaria == 60:
                            qts_matriz[1][1] = qts_segunda
                            qts_matriz[2][1] = qts_segunda
                            qts_matriz[3][1] = qts_segunda
                            qts_matriz[4][1] = '-'
                            
                        elif qts_segunda.disciplina.carga_horaria == 40:
                            qts_matriz[1][1] = qts_segunda
                            qts_matriz[2][1] = qts_segunda

                            for disciplina_segunda2 in disciplinas:
                                for professor_segunda2 in professores:
                                    apt_segunda2 = Disciplina.objects.filter(
                                        Professor = professor_segunda2,
                                        nome=disciplina_segunda2.nome
                                    ).exists()
                                    disponibilidade_segunda2 = Disponibilidade.objects.filter(
                                        professor= professor_segunda2,
                                        semana__dia='seg'
                                    ).first()

                                    if disponibilidade_segunda2 and apt_segunda2:
                                        qts_criado_segunda2 = QTS.objects.filter(
                                            professor= professor_segunda2,
                                            disciplina = disciplina_segunda2,
                                            disponibilidade = disponibilidade_segunda2
                                        ).first()
                                            
                                        if not qts_criado_segunda2:
                                            qts_segunda2 = QTS.objects.create(
                                                professor=professor_segunda2,
                                                disciplina=disciplina_segunda2,
                                                disponibilidade=disponibilidade_segunda2
                                            )
                                        if qts_criado_segunda2:
                                            qts_segunda2 = qts_criado_segunda2
                                        for disciplina_segunda2 in disciplinas:
                                            if qts_segunda2.disciplina.carga_horaria == 40 and qts_matriz[1][1].disciplina != disciplina_segunda2:
                                                qts_matriz[3][1] = qts_segunda2
                                                qts_matriz[4][1] = qts_segunda2
                                                
                                            
            # Dia de terça feira
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


                        if qts_terca.disciplina.carga_horaria == 80:
                            if qts_matriz[3][1].disciplina and qts_matriz[3][1].disciplina != qts_terca.disciplina and qts_matriz[1][1].disciplina != qts_terca.disciplina:
                                qts_matriz[1][2] = qts_terca
                                qts_matriz[2][2] = qts_terca
                                qts_matriz[3][2] = qts_terca
                                qts_matriz[4][2] = qts_terca
                            elif not qts_matriz[3][1].disciplina and qts_matriz[1][1].disciplina != qts_terca.disciplina:
                                qts_matriz[1][2] = qts_terca
                                qts_matriz[2][2] = qts_terca
                                qts_matriz[3][2] = qts_terca
                                qts_matriz[4][2] = qts_terca

                            break
        
                        elif qts_terca.disciplina.carga_horaria == 60:
                            if qts_matriz[3][1].disciplina and qts_matriz[3][1].disciplina != qts_terca.disciplina and qts_matriz[1][1].disciplina != qts_terca.disciplina:
                                qts_matriz[1][2] = qts_terca
                                qts_matriz[2][2] = qts_terca
                                qts_matriz[3][2] = qts_terca
                                qts_matriz[4][2] = '-'
                            elif not qts_matriz[3][1].disciplina and qts_matriz[1][1].disciplina != qts_terca.disciplina:
                                qts_matriz[1][2] = qts_terca
                                qts_matriz[2][2] = qts_terca
                                qts_matriz[3][2] = qts_terca
                                qts_matriz[4][2] = '-'
                            
                        elif qts_terca.disciplina.carga_horaria == 40:
                            if qts_matriz[3][1].disciplina and qts_matriz[3][1].disciplina != qts_terca.disciplina and qts_matriz[1][1].disciplina != qts_terca.disciplina:
                                qts_matriz[1][2] = qts_terca
                                qts_matriz[2][2] = qts_terca
                            elif not qts_matriz[3][1].disciplina and qts_matriz[1][1].disciplina != qts_terca.disciplina:
                                qts_matriz[1][2] = qts_terca
                                qts_matriz[2][2] = qts_terca

                            for disciplina_terca2 in disciplinas:
                                for professor_terca2 in professores:
                                    apt_terca2 = Disciplina.objects.filter(
                                        Professor = professor_terca2,
                                        nome=disciplina_terca2.nome
                                    ).exists()

                                    disponibilidade_terca2 = Disponibilidade.objects.filter(
                                        professor= professor_terca2,
                                        semana__dia='ter'
                                    ).first()

                                    if disponibilidade_terca2 and apt_terca2:
                                        qts_criado_terca2 = QTS.objects.filter(
                                            professor= professor_terca2,
                                            disciplina = disciplina_terca2,
                                            disponibilidade = disponibilidade_terca2
                                        ).first()
                                            
                                        if not qts_criado_terca2:
                                            qts_terca2 = QTS.objects.create(
                                                professor=professor_terca2,
                                                disciplina=disciplina_terca2,
                                                disponibilidade=disponibilidade_terca2
                                            )
                                        if qts_criado_terca2:
                                            qts_terca2 = qts_criado_terca2

                                            if qts_terca2.disciplina.carga_horaria == 40 and not qts_matriz[1][2].disciplina.carga_horaria == 80 and not qts_matriz[1][2].disciplina.carga_horaria == 60:
                                                if qts_matriz[3][1].disciplina and qts_matriz[3][1].disciplina != qts_terca2.disciplina and qts_matriz[1][1].disciplina != qts_terca2.disciplina and qts_matriz[1][2].disciplina != qts_terca2.disciplina:
                                                    qts_matriz[3][2] = qts_terca2
                                                    qts_matriz[4][2] = qts_terca2
                                                elif not qts_matriz[3][1].disciplina and qts_terca2.disciplina.carga_horaria and qts_matriz[1][1].disciplina != qts_terca2.disciplina  and qts_matriz[1][2].disciplina != qts_terca2.disciplina:
                                                    qts_matriz[3][2] = qts_terca2
                                                    qts_matriz[4][2] = qts_terca2
            
            # Dia de quarta-feira

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


                        if qts_quarta.disciplina.carga_horaria == 80:
                            if qts_matriz[3][2].disciplina and qts_matriz[3][1].disciplina != qts_quarta.disciplina and qts_matriz[1][1].disciplina != qts_quarta.disciplina and qts_matriz[3][2].disciplina != qts_quarta.disciplina and qts_matriz[1][2].disciplina != qts_quarta.disciplina:
                                qts_matriz[1][3] = qts_quarta
                                qts_matriz[2][3] = qts_quarta
                                qts_matriz[3][3] = qts_quarta
                                qts_matriz[4][3] = qts_quarta
                            elif not qts_matriz[3][2].disciplina and qts_matriz[1][1].disciplina != qts_quarta.disciplina and qts_matriz[3][1].disciplina != qts_quarta.disciplina and qts_matriz[1][2].disciplina != qts_quarta.disciplina:
                                qts_matriz[1][3] = qts_quarta
                                qts_matriz[2][3] = qts_quarta
                                qts_matriz[3][3] = qts_quarta
                                qts_matriz[4][3] = qts_quarta

                            break
        
                        elif qts_quarta.disciplina.carga_horaria == 60:
                            if qts_matriz[3][2].disciplina and qts_matriz[3][1].disciplina != qts_quarta.disciplina and qts_matriz[1][1].disciplina != qts_quarta.disciplina and qts_matriz[3][2].disciplina != qts_quarta.disciplina and qts_matriz[1][2].disciplina != qts_quarta.disciplina:
                                qts_matriz[1][3] = qts_quarta
                                qts_matriz[2][3] = qts_quarta
                                qts_matriz[3][3] = qts_quarta
                                qts_matriz[4][3] = '-'
                            elif not qts_matriz[3][2].disciplina and qts_matriz[1][1].disciplina != qts_quarta.disciplina and qts_matriz[3][1].disciplina != qts_quarta.disciplina and qts_matriz[1][2].disciplina != qts_quarta.disciplina:
                                qts_matriz[1][3] = qts_quarta
                                qts_matriz[2][3] = qts_quarta
                                qts_matriz[3][3] = qts_quarta
                                qts_matriz[4][3] = '-'

                            
                        elif qts_quarta.disciplina.carga_horaria == 40:
                            if qts_matriz[3][2].disciplina and qts_matriz[3][1].disciplina != qts_quarta.disciplina and qts_matriz[1][1].disciplina != qts_quarta.disciplina and qts_matriz[3][2].disciplina != qts_quarta.disciplina and qts_matriz[1][2].disciplina != qts_quarta.disciplina:
                                qts_matriz[1][3] = qts_quarta
                                qts_matriz[2][3] = qts_quarta
                            elif not qts_matriz[3][2].disciplina and qts_matriz[1][1].disciplina != qts_quarta.disciplina and qts_matriz[3][1].disciplina != qts_quarta.disciplina and qts_matriz[1][2].disciplina != qts_quarta.disciplina:
                                qts_matriz[1][3] = qts_quarta
                                qts_matriz[2][3] = qts_quarta

                            for disciplina_quarta2 in disciplinas:
                                for professor_quarta2 in professores:

                                    apt_quarta2 = Disciplina.objects.filter(
                                        Professor = professor_quarta2,
                                        nome=disciplina_quarta2.nome
                                    ).exists()


                                    disponibilidade_quarta2 = Disponibilidade.objects.filter(
                                        professor= professor_quarta2,
                                        semana__dia='qua'
                                    ).first()

                                    if disponibilidade_quarta2 and apt_quarta2:
                                        qts_criado_quarta2 = QTS.objects.filter(
                                            professor= professor_quarta2,
                                            disciplina = disciplina_quarta2,
                                            disponibilidade = disponibilidade_quarta2
                                        ).first()
                                            
                                        if not qts_criado_quarta2:
                                            qts_quarta2 = QTS.objects.create(
                                                professor=professor_quarta2,
                                                disciplina=disciplina_quarta2,
                                                disponibilidade=disponibilidade_quarta2
                                            )
                                        if qts_criado_quarta2:
                                            qts_quarta2 = qts_criado_quarta2

                                            if qts_quarta2.disciplina.carga_horaria == 40 and not qts_matriz[1][3].disciplina.carga_horaria == 80 and not qts_matriz[1][3].disciplina.carga_horaria == 60:
                                                if qts_matriz[3][2].disciplina and qts_quarta2.disciplina.carga_horaria and qts_matriz[3][1].disciplina != qts_quarta2.disciplina and qts_matriz[1][1].disciplina != qts_quarta2.disciplina and qts_matriz[1][2].disciplina != qts_quarta2.disciplina and qts_matriz[3][2].disciplina != qts_quarta2.disciplina and qts_matriz[1][3].disciplina != qts_quarta2.disciplina:
                                                    qts_matriz[3][3] = qts_quarta2
                                                    qts_matriz[4][3] = qts_quarta2
                                                elif not qts_matriz[3][2].disciplina and qts_quarta2.disciplina.carga_horaria and qts_matriz[1][1].disciplina != qts_quarta2.disciplina  and qts_matriz[3][1].disciplina != qts_quarta2.disciplina and qts_matriz[1][2].disciplina != qts_quarta2.disciplina and qts_matriz[1][3].disciplina != qts_quarta2.disciplina:
                                                    qts_matriz[3][3] = qts_quarta2
                                                    qts_matriz[4][3] = qts_quarta2
                                        
            # Dia de quinta-feira

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


                        if qts_quinta.disciplina.carga_horaria == 80:
                            if qts_matriz[3][3].disciplina and qts_matriz[3][1].disciplina != qts_quinta.disciplina and qts_matriz[1][1].disciplina != qts_quinta.disciplina and qts_matriz[3][2].disciplina != qts_quinta.disciplina and qts_matriz[1][2].disciplina != qts_quinta.disciplina and qts_matriz[3][3].disciplina != qts_quinta.disciplina and qts_matriz[1][3].disciplina != qts_quinta.disciplina:
                                qts_matriz[1][4] = qts_quinta
                                qts_matriz[2][4] = qts_quinta
                                qts_matriz[3][4] = qts_quinta
                                qts_matriz[4][4] = qts_quinta
                            elif not qts_matriz[3][3].disciplina and qts_matriz[3][1].disciplina != qts_quinta.disciplina and qts_matriz[1][1].disciplina != qts_quinta.disciplina and qts_matriz[3][2].disciplina != qts_quinta.disciplina and qts_matriz[1][2].disciplina != qts_quinta.disciplina and qts_matriz[1][3].disciplina != qts_quinta.disciplina:
                                qts_matriz[1][4] = qts_quinta
                                qts_matriz[2][4] = qts_quinta
                                qts_matriz[3][4] = qts_quinta
                                qts_matriz[4][4] = qts_quinta
                            break
        
                        elif qts_quarta.disciplina.carga_horaria == 60:
                            if qts_matriz[3][3].disciplina and qts_matriz[3][1].disciplina != qts_quinta.disciplina and qts_matriz[1][1].disciplina != qts_quinta.disciplina and qts_matriz[3][2].disciplina != qts_quinta.disciplina and qts_matriz[1][2].disciplina != qts_quinta.disciplina and qts_matriz[3][3].disciplina != qts_quinta.disciplina and qts_matriz[1][3].disciplina != qts_quinta.disciplina:
                                qts_matriz[1][4] = qts_quinta
                                qts_matriz[2][4] = qts_quinta
                                qts_matriz[3][4] = qts_quinta
                                qts_matriz[4][4] = '-'
                            elif not qts_matriz[3][3].disciplina and qts_matriz[3][1].disciplina != qts_quinta.disciplina and qts_matriz[1][1].disciplina != qts_quinta.disciplina and qts_matriz[3][2].disciplina != qts_quinta.disciplina and qts_matriz[1][2].disciplina != qts_quinta.disciplina and qts_matriz[1][3].disciplina != qts_quinta.disciplina:
                                qts_matriz[1][4] = qts_quinta
                                qts_matriz[2][4] = qts_quinta
                                qts_matriz[3][4] = qts_quinta
                                qts_matriz[4][4] = '-'

                            
                        elif qts_quinta.disciplina.carga_horaria == 40:
                            if qts_matriz[3][3].disciplina and qts_matriz[3][1].disciplina != qts_quinta.disciplina and qts_matriz[1][1].disciplina != qts_quinta.disciplina and qts_matriz[3][2].disciplina != qts_quinta.disciplina and qts_matriz[1][2].disciplina != qts_quinta.disciplina and qts_matriz[3][3].disciplina != qts_quinta.disciplina and qts_matriz[1][3].disciplina != qts_quinta.disciplina and not qts_matriz[2][4]:
                                qts_matriz[1][4] = qts_quinta
                                qts_matriz[2][4] = qts_quinta
                            elif not qts_matriz[3][3].disciplina and qts_matriz[3][1].disciplina != qts_quinta.disciplina and qts_matriz[1][1].disciplina != qts_quinta.disciplina and qts_matriz[3][2].disciplina != qts_quinta.disciplina and qts_matriz[1][2].disciplina != qts_quinta.disciplina and qts_matriz[1][3].disciplina != qts_quinta.disciplina:
                                qts_matriz[1][4] = qts_quinta
                                qts_matriz[2][4] = qts_quinta

                            for disciplina_quinta2 in disciplinas:
                                for professor_quinta2 in professores:

                                    apt_quinta2 = Disciplina.objects.filter(
                                        Professor = professor_quinta2,
                                        nome=disciplina_quinta2.nome
                                    ).exists()


                                    disponibilidade_quinta2 = Disponibilidade.objects.filter(
                                        professor= professor_quinta2,
                                        semana__dia='qui'
                                    ).first()

                                    if disponibilidade_quinta2 and apt_quinta2:
                                        qts_criado_quinta2 = QTS.objects.filter(
                                            professor= professor_quinta2,
                                            disciplina = disciplina_quinta2,
                                            disponibilidade = disponibilidade_quinta2
                                        ).first()
                                            
                                        if not qts_criado_quinta2:
                                            qts_quinta2 = QTS.objects.create(
                                                professor=professor_quinta2,
                                                disciplina=disciplina_quinta2,
                                                disponibilidade=disponibilidade_quinta2
                                            )
                                        if qts_criado_quinta2:
                                            qts_quinta2 = qts_criado_quinta2

                                            if qts_quinta2.disciplina.carga_horaria == 40:
                                                if qts_matriz[3][3].disciplina and qts_quinta2.disciplina.carga_horaria and qts_matriz[3][1].disciplina != qts_quinta2.disciplina and qts_matriz[1][1].disciplina != qts_quinta2.disciplina and qts_matriz[1][2].disciplina != qts_quinta2.disciplina and qts_matriz[3][2].disciplina != qts_quinta2.disciplina and qts_matriz[1][3].disciplina != qts_quinta2.disciplina and qts_matriz[3][3].disciplina != qts_quinta2.disciplina and qts_matriz[1][4].disciplina != qts_quinta2.disciplina  and not qts_matriz[1][4].disciplina.carga_horaria == 80 and not qts_matriz[1][4].disciplina.carga_horaria == 60:
                                                    qts_matriz[3][4] = qts_quinta2
                                                    qts_matriz[4][4] = qts_quinta2
                                                elif not qts_matriz[3][3].disciplina and qts_quinta2.disciplina.carga_horaria and qts_matriz[1][1].disciplina != qts_quinta2.disciplina  and qts_matriz[3][1].disciplina != qts_quinta2.disciplina and qts_matriz[1][2].disciplina != qts_quinta2.disciplina and qts_matriz[3][2].disciplina != qts_quinta2.disciplina and qts_matriz[1][3].disciplina != qts_quinta2.disciplina and qts_matriz[1][4].disciplina != qts_quinta2.disciplina  and not qts_matriz[1][4].disciplina.carga_horaria == 80 and not qts_matriz[1][4].disciplina.carga_horaria == 60:
                                                    qts_matriz[3][4] = qts_quinta2
                                                    qts_matriz[4][4] = qts_quinta2
                                


                                            
                                                     

                        

                                            

            # Dia de sexta-feira

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


                        if qts_sexta.disciplina.carga_horaria == 80:
                            if qts_matriz[3][4].disciplina and qts_matriz[3][1].disciplina != qts_sexta.disciplina and qts_matriz[1][1].disciplina != qts_sexta.disciplina and qts_matriz[3][2].disciplina != qts_sexta.disciplina and qts_matriz[1][2].disciplina != qts_sexta.disciplina and qts_matriz[3][3].disciplina != qts_sexta.disciplina and qts_matriz[1][3].disciplina != qts_sexta.disciplina and qts_matriz[1][4].disciplina != qts_sexta.disciplina and qts_matriz[3][4].disciplina != qts_sexta.disciplina:
                                qts_matriz[1][5] = qts_sexta
                                qts_matriz[2][5] = qts_sexta
                                qts_matriz[3][5] = qts_sexta
                                qts_matriz[4][5] = qts_sexta
                            elif not qts_matriz[3][4].disciplina and qts_matriz[3][1].disciplina != qts_sexta.disciplina and qts_matriz[1][1].disciplina != qts_sexta.disciplina and qts_matriz[3][2].disciplina != qts_sexta.disciplina and qts_matriz[1][2].disciplina != qts_sexta.disciplina and qts_matriz[3][3].disciplina != qts_sexta.disciplina and qts_matriz[1][3].disciplina != qts_sexta.disciplina and qts_matriz[1][4].disciplina != qts_sexta.disciplina:
                                qts_matriz[1][5] = qts_sexta
                                qts_matriz[2][5] = qts_sexta
                                qts_matriz[3][5] = qts_sexta
                                qts_matriz[4][5] = qts_sexta
        
                        elif qts_sexta.disciplina.carga_horaria == 60:
                            if qts_matriz[3][4].disciplina and qts_matriz[3][1].disciplina != qts_sexta.disciplina and qts_matriz[1][1].disciplina != qts_sexta.disciplina and qts_matriz[3][2].disciplina != qts_sexta.disciplina and qts_matriz[1][2].disciplina != qts_sexta.disciplina and qts_matriz[3][3].disciplina != qts_sexta.disciplina and qts_matriz[1][3].disciplina != qts_sexta.disciplina and qts_matriz[1][4].disciplina != qts_sexta.disciplina and qts_matriz[3][4].disciplina != qts_sexta.disciplina:
                                qts_matriz[1][5] = qts_sexta
                                qts_matriz[2][5] = qts_sexta
                                qts_matriz[3][5] = qts_sexta
                                qts_matriz[4][5] = '-'
                            elif not qts_matriz[3][4].disciplina and qts_matriz[3][1].disciplina != qts_sexta.disciplina and qts_matriz[1][1].disciplina != qts_sexta.disciplina and qts_matriz[3][2].disciplina != qts_sexta.disciplina and qts_matriz[1][2].disciplina != qts_sexta.disciplina and qts_matriz[3][3].disciplina != qts_sexta.disciplina and qts_matriz[1][3].disciplina != qts_sexta.disciplina and qts_matriz[1][4].disciplina != qts_sexta.disciplina:
                                qts_matriz[1][5] = qts_sexta
                                qts_matriz[2][5] = qts_sexta
                                qts_matriz[3][5] = qts_sexta
                                qts_matriz[4][5] = '-'

                            
                        elif qts_sexta.disciplina.carga_horaria == 40:
                            if qts_matriz[3][4].disciplina and qts_matriz[3][1].disciplina != qts_sexta.disciplina and qts_matriz[1][1].disciplina != qts_sexta.disciplina and qts_matriz[3][2].disciplina != qts_sexta.disciplina and qts_matriz[1][2].disciplina != qts_sexta.disciplina and qts_matriz[3][3].disciplina != qts_sexta.disciplina and qts_matriz[1][3].disciplina != qts_sexta.disciplina and qts_matriz[1][4].disciplina != qts_sexta.disciplina and qts_matriz[3][4].disciplina != qts_sexta.disciplina:
                                qts_matriz[1][5] = qts_sexta
                                qts_matriz[2][5] = qts_sexta
                            elif not qts_matriz[3][4].disciplina and qts_matriz[3][1].disciplina != qts_sexta.disciplina and qts_matriz[1][1].disciplina != qts_sexta.disciplina and qts_matriz[3][2].disciplina != qts_sexta.disciplina and qts_matriz[1][2].disciplina != qts_sexta.disciplina and qts_matriz[3][3].disciplina != qts_sexta.disciplina and qts_matriz[1][3].disciplina != qts_sexta.disciplina and qts_matriz[1][4].disciplina != qts_sexta.disciplina:
                                qts_matriz[1][5] = qts_sexta
                                qts_matriz[2][5] = qts_sexta

                            for disciplina_sexta2 in disciplinas:
                                for professor_sexta2 in professores:

                                    apt_sexta2 = Disciplina.objects.filter(
                                        Professor = professor_sexta2,
                                        nome=disciplina_sexta2.nome
                                    ).exists()


                                    disponibilidade_sexta2 = Disponibilidade.objects.filter(
                                        professor= professor_sexta2,
                                        semana__dia='sex'
                                    ).first()

                                    if disponibilidade_sexta2 and apt_sexta2:
                                        qts_criado_sexta2 = QTS.objects.filter(
                                            professor= professor_sexta2,
                                            disciplina = disciplina_sexta2,
                                            disponibilidade = disponibilidade_sexta2
                                        ).first()
                                            
                                        if not qts_criado_sexta2:
                                            qts_sexta2 = QTS.objects.create(
                                                professor=professor_sexta2,
                                                disciplina=disciplina_sexta2,
                                                disponibilidade=disponibilidade_sexta2
                                            )
                                        if qts_criado_sexta2:
                                            qts_sexta2 = qts_criado_sexta2

                                            if qts_sexta2.disciplina.carga_horaria == 40:
                                                if qts_matriz[3][4].disciplina and qts_sexta2.disciplina.carga_horaria and qts_matriz[3][1].disciplina != qts_sexta2.disciplina and qts_matriz[1][1].disciplina != qts_sexta2.disciplina and qts_matriz[1][2].disciplina != qts_sexta2.disciplina and qts_matriz[3][2].disciplina != qts_sexta2.disciplina and qts_matriz[1][3].disciplina != qts_sexta2.disciplina and qts_matriz[3][3].disciplina != qts_sexta2.disciplina and qts_matriz[1][4].disciplina != qts_sexta2.disciplina and qts_matriz[3][4].disciplina != qts_sexta2.disciplina and qts_matriz[1][5].disciplina != qts_sexta2.disciplina  and not qts_matriz[1][5].disciplina.carga_horaria == 80 and not qts_matriz[1][5].disciplina.carga_horaria == 60:
                                                    qts_matriz[3][5] = qts_sexta2
                                                    qts_matriz[4][5] = qts_sexta2
                                                elif not qts_matriz[3][4].disciplina and qts_sexta2.disciplina.carga_horaria and qts_matriz[3][1].disciplina != qts_sexta2.disciplina and qts_matriz[1][1].disciplina != qts_sexta2.disciplina and qts_matriz[1][2].disciplina != qts_sexta2.disciplina and qts_matriz[3][2].disciplina != qts_sexta2.disciplina and qts_matriz[1][3].disciplina != qts_sexta2.disciplina and qts_matriz[3][3].disciplina != qts_sexta2.disciplina and qts_matriz[1][4].disciplina != qts_sexta2.disciplina and qts_matriz[1][5].disciplina != qts_sexta2.disciplina  and not qts_matriz[1][5].disciplina.carga_horaria == 80 and not qts_matriz[1][5].disciplina.carga_horaria == 60:
                                                    qts_matriz[3][5] = qts_sexta2
                                                    qts_matriz[4][5] = qts_sexta2
                                            


            qts_matrices[i] = qts_matriz
    
        return qts_matrices

