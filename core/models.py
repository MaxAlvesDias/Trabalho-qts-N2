from django.db import models
from stdimage.models import StdImageField

class Base(models.Model):
    criado_em = models.DateField('criação', auto_now_add= True)
    modificado_em = models.DateField('atualização', auto_now= True)
    ativo = models.BooleanField('ativo', default = True)

    class Meta:
        abstract = True

class DiasSemana(Base):
    Dias_Choices = [
        ('seg', 'Segunda-feira'),
        ('ter', 'Terça-feira'),
        ('qua', 'Quarta-feira'),
        ('qui', 'Quinta-feira'),
        ('sex', 'Sexta-feira'),
    ]
    dia = models.CharField('Dia', max_length=3, choices=Dias_Choices)
    horario_1_inicio = models.TimeField('1º Horário de início', default=None, null=True, blank=True)
    horario_1_fim = models.TimeField('1º Horário de fim', default=None, null=True, blank=True)
    horario_2_inicio = models.TimeField('2º Horário de início', default=None, null=True, blank=True)
    horario_2_fim = models.TimeField('2º Horário de fim', default=None, null=True, blank=True)
    horario_3_inicio = models.TimeField('3º Horário de início', default=None, null=True, blank=True)
    horario_3_fim = models.TimeField('3º Horário de fim', default=None, null=True, blank=True)
    horario_4_inicio = models.TimeField('4º Horário de início', default=None, null=True, blank=True)
    horario_4_fim = models.TimeField('4º Horário de fim', default=None, null=True, blank=True)

    def __str__(self):
        horarios = [self.horario_1_inicio, self.horario_1_fim,
                    self.horario_2_inicio, self.horario_2_fim,
                    self.horario_3_inicio, self.horario_3_fim,
                    self.horario_4_inicio, self.horario_4_fim]
        horarios_str = [f"{inicio.strftime('%H:%M')} às {fim.strftime('%H:%M')}" if inicio and fim else '' 
                        for inicio, fim in zip(horarios[::2], horarios[1::2])]
        return f"{self.get_dia_display()} - {' - '.join(horarios_str)}"       
        
        

class Disciplina(Base):
    nome = models.CharField('Nome',max_length=100)
    carga_horaria = models.IntegerField('Carga horaria')
    professor = models.ForeignKey('core.Professor', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Professor')

    class Meta:
        verbose_name= 'Disciplina'

    def __str__(self):
        return self.nome


class Professor(Base):
    nome = models.CharField('Nome', max_length=100)
    bio = models.TextField('Bio', max_length= 200)
    imagem = StdImageField('Imagem', upload_to = 'professor', variations= {'thumb':{'width': 200,'height':200,'crop':True}})
    disponibilidade = models.ManyToManyField(DiasSemana, verbose_name='Disponibilidade')
    facebook = models.CharField('facebook',max_length=100,default='#')
    instagram = models.CharField('instagram',max_length=100,default='#')
    linkedin = models.CharField('linkedIn',max_length=100,default='#')
    x = models.CharField('x',max_length=100,default='#')

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

    def __str__(self):
        return self.nome
