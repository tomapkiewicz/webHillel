# Generated by Django 3.1.7 on 2021-06-29 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0020_auto_20210629_0149'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='nuevo',
            field=models.BooleanField(default=0, verbose_name='Nuevo: Tildado - Regular: Destildado'),
        ),
    ]