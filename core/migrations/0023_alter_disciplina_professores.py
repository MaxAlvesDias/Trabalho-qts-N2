from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_qts_disciplina_professores'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disciplina',
            name='professores',
        ),
        migrations.AddField(
            model_name='disciplina',
            name='professores',
            field=models.ManyToManyField(to='core.Professor', verbose_name='Professores'),
        ),
    ]
