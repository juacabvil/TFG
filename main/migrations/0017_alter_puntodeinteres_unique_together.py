# Generated by Django 4.2.3 on 2023-09-23 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_puntousuario_asistencia_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='puntodeinteres',
            unique_together={('latitud', 'longitud')},
        ),
    ]
