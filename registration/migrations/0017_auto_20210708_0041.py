# Generated by Django 3.1.7 on 2021-07-08 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0016_auto_20210708_0034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='link',
        ),
        migrations.AlterField(
            model_name='profile',
            name='apellido',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='celular',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Número de Whatsapp'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='comoConociste',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='¿Cómo conociste Hillel?'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='estudios',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='¿Estás estudiando, o te recibiste? ¿Qué estudias/te y en qué institución?'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='experienciaComunitaria',
            field=models.URLField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='instagram',
            field=models.URLField(blank=True, max_length=100, null=True, verbose_name='@ de Instagram'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]