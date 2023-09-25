# Generated by Django 4.2.3 on 2023-09-22 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_puntodeinteres_accesibilidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='PuntoUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('amenidad', models.CharField(choices=[('Comida', 'Comida'), ('Entretenimiento', 'Entretenimiento'), ('Servicios Financieros', 'Servicios Financieros'), ('Bebidas', 'Bebidas'), ('Salud', 'Salud'), ('Educación', 'Educación'), ('Cultura y Arte', 'Cultura y Arte'), ('Servicios Públicos', 'Servicios Públicos'), ('Transporte', 'Transporte'), ('Otros', 'Otros'), ('Baños', 'Baños'), ('Fuel', 'Fuel'), ('Desconocida', 'Desconocida')], default='Desconocida', max_length=100)),
                ('color_accesibilidad', models.CharField(choices=[('red', 'Red'), ('orange', 'Orange'), ('green', 'Green'), ('blue', 'Blue')], default='red', max_length=10)),
                ('wcAdaptado', models.BooleanField(default=False)),
                ('AnimalesGuia', models.BooleanField(default=False)),
            ],
        ),
    ]