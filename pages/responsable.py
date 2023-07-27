from django.db import models


class Responsable(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=200)

    def __str__(self):
        return self.nombre
