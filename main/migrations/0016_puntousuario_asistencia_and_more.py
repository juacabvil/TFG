# Generated by Django 4.2.3 on 2023-09-23 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_puntousuario_descripcion_puntousuario_nombre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='puntousuario',
            name='Asistencia',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='puntodeinteres',
            name='descripcion',
            field=models.TextField(max_length=2000),
        ),
    ]