# Generated by Django 5.1.6 on 2025-03-10 19:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Personaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('imagen', models.ImageField(upload_to='personajes/')),
                ('personalidad', models.TextField(help_text='Descripción de la personalidad para generar respuestas')),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Conversacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('titulo', models.CharField(default='Nueva conversación', max_length=200)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('personaje', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot.personaje')),
            ],
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('tipo', models.CharField(choices=[('usuario', 'Usuario'), ('personaje', 'Personaje')], max_length=10)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('conversacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensajes', to='chatbot.conversacion')),
            ],
            options={
                'ordering': ['fecha'],
            },
        ),
    ]
