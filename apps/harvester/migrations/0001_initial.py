# Generated by Django 3.2.5 on 2021-08-09 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MProxysAlmacenados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=120)),
                ('puerto', models.CharField(max_length=120)),
                ('protocolo', models.CharField(max_length=120)),
                ('estado', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='MProxysDisponibles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=120)),
                ('puerto', models.CharField(max_length=120)),
                ('protocolo', models.CharField(max_length=120)),
            ],
        ),
    ]
