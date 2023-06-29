from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class CuestionarioRespuestaManager(models.Manager):

    def find(self, user, page):
        queryset = self.filter(user=user, page=page)
        if len(queryset) > 0:
            return queryset[0]
        return None

    def find_or_create(self, user, page):
        cuestionarioRespuesta = self.find(user=user, page=page)
        if cuestionarioRespuesta is None:
            print("se crea")
            print(user)
            print(page)

            cuestionarioRespuesta = CuestionarioRespuesta.objects.create(user=user, page=page)
        return cuestionarioRespuesta


class CuestionarioRespuesta(models.Model):
    page = models.ForeignKey('Page', related_name="pagina_cuestionario_respuesta", verbose_name='Actividad', null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)
    pregunta1 = models.CharField(verbose_name="Pregunta1", null=True, blank=True, default="", max_length=200)
    respuesta1 = models.CharField(verbose_name="Respuesta1", null=True, blank=True, default="", max_length=200)
    pregunta2 = models.CharField(verbose_name="Pregunta2", null=True, blank=True, default="", max_length=200)
    respuesta2 = models.CharField(verbose_name="Respuesta2", null=True, blank=True, default="", max_length=200)
    pregunta3 = models.CharField(verbose_name="Pregunta3", null=True, blank=True, default="", max_length=200)
    respuesta3 = models.CharField(verbose_name="Respuesta3", null=True, blank=True, default="", max_length=200)
    pregunta4 = models.CharField(verbose_name="Pregunta4", null=True, blank=True, default="", max_length=200)
    respuesta4 = models.CharField(verbose_name="Respuesta4", null=True, blank=True, default="", max_length=200)
    pregunta5 = models.CharField(verbose_name="Pregunta5", null=True, blank=True, default="", max_length=200)
    respuesta5 = models.CharField(verbose_name="Respuesta5", null=True, blank=True, default="", max_length=200)
    pregunta6 = models.CharField(verbose_name="Pregunta6", null=True, blank=True, default="", max_length=200)
    respuesta6 = models.CharField(verbose_name="Respuesta6", null=True, blank=True, default="", max_length=200)
    pregunta7 = models.CharField(verbose_name="Pregunta7", null=True, blank=True, default="", max_length=200)
    respuesta7 = models.CharField(verbose_name="Respuesta7", null=True, blank=True, default="", max_length=200)
    pregunta8 = models.CharField(verbose_name="Pregunta8", null=True, blank=True, default="", max_length=200)
    respuesta8 = models.CharField(verbose_name="Respuesta8", null=True, blank=True, default="", max_length=200)
    pregunta9 = models.CharField(verbose_name="Pregunta9", null=True, blank=True, default="", max_length=200)
    respuesta9 = models.CharField(verbose_name="Respuesta9", null=True, blank=True, default="", max_length=200)
    pregunta10 = models.CharField(verbose_name="Pregunta10", null=True, blank=True, default="", max_length=200)
    respuesta10 = models.CharField(verbose_name="Respuesta10", null=True, blank=True, default="", max_length=200)
    pregunta11 = models.CharField(verbose_name="Pregunta11", null=True, blank=True, default="", max_length=200)
    respuesta11 = models.CharField(verbose_name="Respuesta11", null=True, blank=True, default="", max_length=200)
    pregunta12 = models.CharField(verbose_name="Pregunta12", null=True, blank=True, default="", max_length=200)
    respuesta12 = models.CharField(verbose_name="Respuesta12", null=True, blank=True, default="", max_length=200)
    pregunta13 = models.CharField(verbose_name="Pregunta13", null=True, blank=True, default="", max_length=200)
    respuesta13 = models.CharField(verbose_name="Respuesta13", null=True, blank=True, default="", max_length=200)
    pregunta14 = models.CharField(verbose_name="Pregunta14", null=True, blank=True, default="", max_length=200)
    respuesta14 = models.CharField(verbose_name="Respuesta14", null=True, blank=True, default="", max_length=200)
    pregunta15 = models.CharField(verbose_name="Pregunta15", null=True, blank=True, default="", max_length=200)
    respuesta15 = models.CharField(verbose_name="Respuesta15", null=True, blank=True, default="", max_length=200)
    pregunta16 = models.CharField(verbose_name="Pregunta16", null=True, blank=True, default="", max_length=200)
    respuesta16 = models.CharField(verbose_name="Respuesta16", null=True, blank=True, default="", max_length=200)
    pregunta17 = models.CharField(verbose_name="Pregunta17", null=True, blank=True, default="", max_length=200)
    respuesta17 = models.CharField(verbose_name="Respuesta17", null=True, blank=True, default="", max_length=200)
    pregunta18 = models.CharField(verbose_name="Pregunta18", null=True, blank=True, default="", max_length=200)
    respuesta18 = models.CharField(verbose_name="Respuesta18", null=True, blank=True, default="", max_length=200)
    pregunta19 = models.CharField(verbose_name="Pregunta19", null=True, blank=True, default="", max_length=200)
    respuesta19 = models.CharField(verbose_name="Respuesta19", null=True, blank=True, default="", max_length=200)
    pregunta20 = models.CharField(verbose_name="Pregunta20", null=True, blank=True, default="", max_length=200)
    respuesta20 = models.CharField(verbose_name="Respuesta20", null=True, blank=True, default="", max_length=200)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", blank=True, null=True)
    objects = CuestionarioRespuestaManager()

    class Meta:
        verbose_name = "Cuestionario Respuesta"
        verbose_name_plural = "Cuestionario Respuestas"
        ordering = ['updated']

    def __str__(self):
        return self.page.title + ' Respuestas de ' + self.user.username


class CuestionarioManager(models.Manager):

    def find(self, page):
        queryset = self.filter(page=page)
        print(queryset)
        if len(queryset) > 0:
            return queryset[0]
        return None

    def find_or_create(self, page):
        cuestionario = self.find(page=page)
        if cuestionario is None:
            cuestionario = Cuestionario.objects.create(page=page)
        return cuestionario


class Cuestionario(models.Model):
    page = models.ForeignKey('Page', related_name="pagina_cuestionario", verbose_name='Actividad', null=True, on_delete=models.CASCADE)
    pregunta1 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta2 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta3 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta4 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta5 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta6 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta7 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta8 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta9 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta10 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta11 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta12 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta13 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta14 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta15 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta16 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta17 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta18 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta19 = models.CharField(null=True, blank=True, default="", max_length=200)
    pregunta20 = models.CharField(null=True, blank=True, default="", max_length=200)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", blank=True, null=True)
    objects = CuestionarioManager()

    class Meta:
        verbose_name = "Cuestionario"
        verbose_name_plural = "Cuestionarios"
        ordering = ['updated']

    def __str__(self):
        return self.page.title + ' Preguntas'
