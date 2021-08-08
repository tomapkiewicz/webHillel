from django.db import models

# Create your models here.
class Provincia(models.Model):
    title = models.CharField(verbose_name="Nombre", max_length=200)
    order = models.SmallIntegerField(verbose_name="Orden")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", blank=True, null=True)

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        ordering = ['order']

    def __str__(self):
        return self.title
        