# Generated by Django 4.2.3 on 2023-09-17 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_puntodeinteres_tipo_amenidad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='puntodeinteres',
            name='enlace',
        ),
        migrations.RemoveField(
            model_name='puntodeinteres',
            name='imagen',
        ),
        migrations.AddField(
            model_name='puntodeinteres',
            name='datos_adicionales',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='puntodeinteres',
            name='latitud',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='puntodeinteres',
            name='longitud',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='puntodeinteres',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
    ]
