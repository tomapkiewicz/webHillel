# Generated by Django 3.1.7 on 2021-06-28 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0013_day'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='day',
            options={'ordering': ['order'], 'verbose_name': 'Día', 'verbose_name_plural': 'Días'},
        ),
        migrations.AddField(
            model_name='page',
            name='modalidad',
            field=models.BooleanField(default=0, verbose_name='Modalidad: 0-Presencial 1-Online'),
        ),
    ]
