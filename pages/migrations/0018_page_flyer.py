# Generated by Django 3.1.7 on 2021-06-29 04:27

from django.db import migrations, models
import pages.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0017_auto_20210628_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='flyer',
            field=models.ImageField(blank=True, null=True, upload_to=pages.models.custom_upload_to),
        ),
    ]