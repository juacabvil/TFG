# Generated by Django 4.2.3 on 2023-09-19 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_puntodeinteres_icono'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='puntodeinteres',
            name='icono',
        ),
        migrations.AddField(
            model_name='puntodeinteres',
            name='datos_adicionales',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
