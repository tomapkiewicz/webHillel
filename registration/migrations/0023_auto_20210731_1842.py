# Generated by Django 3.1.7 on 2021-07-31 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
        ('registration', '0022_auto_20210731_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='provincia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.provincia', verbose_name='¿En dónde vivís?'),
        ),
        migrations.DeleteModel(
            name='Provincia',
        ),
    ]
