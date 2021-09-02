from django.db import models


# Create your models here.
class Link(models.Model):
    key = models.SlugField(verbose_name='Nombre clave', max_length=100, unique=True)
    name = models.CharField(verbose_name='Red social', max_length=200)
    url = models.URLField(verbose_name='Enlace', max_length=200, blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de modificación")
    created = models.DateTimeField(auto_now=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "enlace"
        verbose_name_plural = "enlaces"
        ordering = ["name"]

    def __str__(self):
        return self.name

# Create your models here.


class Whatsapp(models.Model):
    numero = models.CharField(verbose_name='Numero ej: 1112341234', max_length=100, unique=True)
    name = models.CharField(verbose_name='Nombre', max_length=200)
    updated = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de modificación")
    created = models.DateTimeField(auto_now=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "whatsapp Hillel"
        verbose_name_plural = "whatsapp Hillel"
        ordering = ["name"]

    def __str__(self):
        return self.numero

# Create your models here.


class MailContacto(models.Model):
    mail = models.CharField(verbose_name='mails ej: uno@uno.com; otro@otro.com; etc.', max_length=100, unique=True)
    updated = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de modificación")
    created = models.DateTimeField(auto_now=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "mail Hillel"
        verbose_name_plural = "mail Hillel"
        ordering = ["mail"]

    def __str__(self):
        return self.mail
