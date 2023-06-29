from django.db import models
from django.contrib.auth.models import User
from .subscription import Subscription


class HistorialManager(models.Manager):

    def find_or_create(self, page, date):
        historial = self.find(page, date)
        if historial is None:
            historial = Historial.objects.create(page=page, fecha=date)
        subscribers = Subscription.objects.find_page(page)
        if subscribers is None:
            return historial
        for subscripcion in subscribers:
            historial.anotados.add(subscripcion.user)
        return historial

    def find(self, page, date):
        historial = self.filter(page=page,
                                fecha__year=date.year,
                                fecha__month=date.month
                                )
        if len(historial) == 0:
            return None
        return historial[0]

    def find_page(self, page):
        historial = self.filter(page=page)
        if len(historial) == 0:
            return None
        return historial


class Historial(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de realización", blank=True, null=True)
    page = models.ForeignKey('Page', related_name="pagina", verbose_name='Actividad', null=True, on_delete=models.CASCADE)
    anotados = models.ManyToManyField(User, related_name="get_anotados", blank=True)
    asistentes = models.ManyToManyField(User, related_name="get_asistencias", blank=True)
    objects = HistorialManager()

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        ordering = ['-fecha', 'page']

    def __str__(self):
        if self.page is None:
            return 'Sin datos.'
        return self.page.title + ' ' + str(self.fecha)

    @property
    def Qasistentes(self):
        asistentes_count = self.asistentes.count()
        if asistentes_count > 0:
            return asistentes_count
        else:
            return 0

    @property
    def Qanotados(self):
        return self.anotados.count()
