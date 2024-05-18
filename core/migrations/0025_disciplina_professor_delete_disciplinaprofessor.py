# Generated by Django 5.0.6 on 2024-05-18 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_remove_disciplina_professores_disciplinaprofessor'),
    ]

    operations = [
        migrations.AddField(
            model_name='disciplina',
            name='Professor',
            field=models.ManyToManyField(related_name='disciplinas', to='core.professor', verbose_name='Professores'),
        ),
        migrations.DeleteModel(
            name='DisciplinaProfessor',
        ),
    ]
