# Generated by Django 3.1.7 on 2021-08-04 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0046_auto_20210731_1903'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='colaborador',
            options={'verbose_name': 'Colaborador', 'verbose_name_plural': 'Colaboradores'},
        ),
        migrations.AddField(
            model_name='page',
            name='pregunta',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Pregunta'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='pregunta',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Pregunta'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='respuesta',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Respuesta'),
        ),
        migrations.AlterField(
            model_name='page',
            name='secreta',
            field=models.BooleanField(default=0, verbose_name='Tiene clave?'),
        ),
    ]