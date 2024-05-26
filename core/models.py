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

    def __str__(self):
        return self.get_dia_display()

class Horario(Base):
    periodo_choices = [
        ('1º Período', '1º Período'),
        ('2º Período', '2º Período'),
        ('3º Período', '3º Período'),
        ('4º Período', '4º Período'),
    ]
    periodo = models.CharField('Período', max_length=20, choices=periodo_choices)
    inicio = models.TimeField('Horário de início')
    fim = models.TimeField('Horário de fim')

    def __str__(self):
        return f"{self.get_periodo_display()}: {self.inicio.strftime('%H:%M')} - {self.fim.strftime('%H:%M')}"
        
        

class Professor(Base):
    nome = models.CharField('Nome', max_length=100)
    bio = models.TextField('Bio', max_length= 200)
    imagem = StdImageField('Imagem', upload_to = 'professor', variations= {'thumb':{'width': 200,'height':200,'crop':True}})
    facebook = models.CharField('facebook',max_length=100,default='#')
    instagram = models.CharField('instagram',max_length=100,default='#')
    linkedin = models.CharField('linkedIn',max_length=100,default='#')
    x = models.CharField('x',max_length=100,default='#')

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

    def __str__(self):
        return self.nome

class Disciplina(Base):
    nome = models.CharField('Nome',max_length=100)
    carga_horaria = models.IntegerField('Carga horaria')
    Professor = models.ManyToManyField(Professor, verbose_name='Professores', related_name='disciplinas')

    class Meta:
        verbose_name= 'Disciplina'
        verbose_name_plural = 'Disciplinas'

    def __str__(self):
        return self.nome



class turma(Base):
    numero = models.IntegerField('Quantidade', default= True)

class Disponibilidade(Base):
    semana = models.ManyToManyField(DiasSemana, verbose_name='Disponibilidade')
    professor = models.ForeignKey(Professor, verbose_name='Professor', on_delete= models.CASCADE, default= True)

    def __str__(self):
        return self.get_professores()

    def get_professores(self):
        return ", ".join([self.professor.nome])
    
class QTS(Base):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    disponibilidade = models.ForeignKey(Disponibilidade, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.professor.nome} - {self.disciplina.nome}"

