# Generated by Django 3.1.7 on 2021-07-04 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0033_auto_20210703_0316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historial',
            name='anotados',
        ),
    ]