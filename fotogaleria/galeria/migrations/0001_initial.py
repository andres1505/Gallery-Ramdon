# Generated by Django 5.1.6 on 2025-03-09 04:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('imagen', models.ImageField(upload_to='fotos/')),
                ('fecha_subida', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Foto',
                'verbose_name_plural': 'Fotos',
                'ordering': ['-fecha_subida'],
            },
        ),
    ]
