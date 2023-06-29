from django.db import models


class Colaborador(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=200)

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"

    def __str__(self):
        return self.nombre