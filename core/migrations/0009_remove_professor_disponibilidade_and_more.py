import django.db.models.deletion
from django.db import migrations, models

def set_default_disponibilidade(apps, schema_editor):
    Professor = apps.get_model('core', 'Professor')
    DiasSemana = apps.get_model('core', 'DiasSemana')
    
    # Defina um valor padrão apropriado. Suponha que exista um registro padrão em DiasSemana
    default_disponibilidade = DiasSemana.objects.first()
    if not default_disponibilidade:
        default_disponibilidade = DiasSemana.objects.create(name='Default')  # Crie um valor padrão se não existir

    # Atualize todos os registros de Professor que têm disponibilidade_id como None
    Professor.objects.filter(disponibilidade_id__isnull=True).update(disponibilidade=default_disponibilidade)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_horario_periodo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professor',
            name='disponibilidade',
        ),
        migrations.AddField(
            model_name='professor',
            name='disponibilidade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.diassemana', verbose_name='Disponibilidade'),
        ),
        migrations.RunPython(set_default_disponibilidade),
        migrations.AlterField(
            model_name='professor',
            name='disponibilidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.diassemana', verbose_name='Disponibilidade'),
        ),
    ]
