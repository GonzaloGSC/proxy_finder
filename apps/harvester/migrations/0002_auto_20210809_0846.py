# Generated by Django 3.2.5 on 2021-08-09 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harvester', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mproxysalmacenados',
            name='fecha',
            field=models.CharField(default='HOLA', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mproxysdisponibles',
            name='fecha',
            field=models.CharField(default='DIOSSS', max_length=120),
            preserve_default=False,
        ),
    ]
