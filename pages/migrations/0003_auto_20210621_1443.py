# Generated by Django 3.1.7 on 2021-06-21 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20210620_1538'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pageslog',
            old_name='pages',
            new_name='page',
        ),
        migrations.RenameField(
            model_name='pageslog',
            old_name='users',
            new_name='user',
        ),
    ]
