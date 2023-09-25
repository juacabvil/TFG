# Generated by Django 4.2.3 on 2023-09-23 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_puntousuario_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puntousuario',
            name='color_accesibilidad',
            field=models.CharField(choices=[('red', 'red'), ('orange', 'orange'), ('green', 'green'), ('blue', 'blue')], default='red', max_length=10),
        ),
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('aparcamiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.aparcamiento')),
                ('punto_interes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.puntodeinteres')),
                ('punto_usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.puntousuario')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
