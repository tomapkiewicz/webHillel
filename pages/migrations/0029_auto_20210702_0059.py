# Generated by Django 3.1.7 on 2021-07-02 00:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0028_auto_20210702_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='dia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pages.day', verbose_name='dia'),
        ),
    ]
