# Generated by Django 3.2.6 on 2021-08-14 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0059_auto_20210809_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='flyer',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
