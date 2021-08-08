# Generated by Django 3.1.7 on 2021-07-08 00:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0014_profile_validado'),
    ]

    operations = [
        migrations.CreateModel(
            name='FechaOnward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.CharField(max_length=200, verbose_name='Fecha')),
                ('order', models.SmallIntegerField(verbose_name='Orden')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de edición')),
            ],
            options={
                'verbose_name': 'FechaOnward',
                'verbose_name_plural': 'FechasOnward',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='FechaTaglit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.CharField(max_length=200, verbose_name='Fecha')),
                ('order', models.SmallIntegerField(verbose_name='Orden')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de edición')),
            ],
            options={
                'verbose_name': 'FechaTaglit',
                'verbose_name_plural': 'FechasTaglit',
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='comoConociste',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='¿Cómo conociste Hillel?'),
        ),
        migrations.AddField(
            model_name='profile',
            name='estudios',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='¿Estás estudiando, o te recibiste? ¿Qué estudias/te y en qué institución?'),
        ),
        migrations.AddField(
            model_name='profile',
            name='experienciaComunitaria',
            field=models.URLField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram',
            field=models.URLField(blank=True, max_length=20, null=True, verbose_name='@ de Instagram'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='dni',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='Número de Whatsapp'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='provincia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.provincia', verbose_name='¿En dónde vivís?'),
        ),
        migrations.AddField(
            model_name='profile',
            name='onward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.fechaonward', verbose_name='¿Viajaste a Onward? ¿Cuándo?'),
        ),
        migrations.AddField(
            model_name='profile',
            name='taglit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.fechataglit', verbose_name='¿Viajaste a Taglit? ¿Cuándo?'),
        ),
    ]