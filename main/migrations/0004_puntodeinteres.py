# Generated by Django 4.1.3 on 2023-09-17 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_usuario_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='PuntoDeInteres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('latitud', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitud', models.DecimalField(decimal_places=6, max_digits=9)),
                ('descripcion', models.TextField()),
                ('imagen', models.ImageField(upload_to='puntos_de_interes/')),
                ('enlace', models.URLField()),
            ],
        ),
    ]
