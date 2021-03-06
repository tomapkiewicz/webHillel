# Generated by Django 3.1.7 on 2021-07-06 00:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0038_auto_20210705_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historial',
            name='anotados',
            field=models.ManyToManyField(blank=True, related_name='get_suscripciones', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='historial',
            name='asistentes',
            field=models.ManyToManyField(blank=True, related_name='get_asistencias', to=settings.AUTH_USER_MODEL),
        ),
    ]
