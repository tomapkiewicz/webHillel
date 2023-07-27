from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="titulo")
    updated = models.DateTimeField(auto_now_add=True, verbose_name="modificado")
    created = models.DateTimeField(auto_now=True, verbose_name="creado")

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
        ordering = ["-created"]

    def __str__(self):
        return self.name
