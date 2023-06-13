from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField

from datetime import datetime
from location.models import Provincia

def custom_upload_to(instance, filename):
    old_instance = Page.objects.filter(pk=instance.pk).first()
    if old_instance is not None:
        old_instance.flyer.delete()
    return 'pages/' + filename


class Responsable(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=200)

    def __str__(self):
        return self.nombre


class Colaborador(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=200)

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"

    def __str__(self):
        return self.nombre


class Day(models.Model):
    day = models.CharField(verbose_name="Día", max_length=200)
    order = models.SmallIntegerField(verbose_name="Orden", default=0)

    class Meta:
        verbose_name = "Día"
        verbose_name_plural = "Días"
        ordering = ['order']

    @property
    def HayActividadPresencial(self, **kwargs):
        pages = Page.objects.find(self, 0)
        if pages is None:
            return False
        return True

    def HayActividadPresencial_provincia(self, provincia):
        pages = Page.objects.find_provincia(self, 0, provincia)
        if pages is None:
            return False
        return True

    @property
    def HayActividadOnline(self):
        pages = Page.objects.find(self, 1)
        if pages is None:
            return False
        return True

    def __str__(self):
        return self.day


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='titulo')
    updated = models.DateTimeField(auto_now_add=True, verbose_name="modificado")
    created = models.DateTimeField(auto_now=True, verbose_name="creado")

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
        ordering = ["-created"]

    def __str__(self):
        return self.name


class PagesManager(models.Manager):

    def find(self, dia, modalidad):
        queryset = self.filter(modalidad=modalidad, dia=dia, activa=True)
        if len(queryset) > 0:
            return queryset
        return None

    def find_provincia(self, dia, modalidad, provincia):
        queryset = self.filter(modalidad=modalidad, dia=dia, activa=True, provincia=provincia)
        if len(queryset) > 0:
            return queryset
        return None


class Page(models.Model):
    title = models.CharField(verbose_name="Título", max_length=200)
    horaDesde = models.TimeField(verbose_name="Hora desde", null=True, blank=True, auto_now=False, auto_now_add=False,)
    horaHasta = models.TimeField(verbose_name="Hora hasta", null=True, blank=True, auto_now=False, auto_now_add=False,)
    description = RichTextField(verbose_name="Descripción", null=True, blank=True)
    textoExtraMail = RichTextField(verbose_name="Texto extra del mail", null=True, blank=True)
    con_mail_personalizado = BooleanField(verbose_name="Tiene mail personalizado?", default=False)
    asunto_mail = models.CharField(verbose_name="Asunto del mail", null=True, blank=True, default="", max_length=200)
    cuerpo_mail= RichTextField(verbose_name="Cuerpo del mail", null=True, blank=True)

    flyer = models.ImageField(upload_to=custom_upload_to,
                              null=True, blank=True)
    dia = models.ForeignKey(Day, verbose_name='dia', null=True, on_delete=models.CASCADE)
    cupo = models.SmallIntegerField(verbose_name="Cupo", default=0)
    modalidad = BooleanField(verbose_name="Online", default=0)
    nuevo = BooleanField(verbose_name="Nuevo", default=0)
    activa = BooleanField(verbose_name="Activa", default=1)
    categories = models.ManyToManyField(Category, verbose_name='categorias', related_name='get_pages', blank=True)

    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, null=True, blank=True)
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE, null=True, blank=True)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, null=True, blank=True)

    secreta = BooleanField(verbose_name="Tiene clave?", default=0)
    clave = models.CharField(verbose_name="Clave", null=True, blank=True, default="", max_length=200)
    con_preinscripcion = BooleanField(verbose_name="Tiene preinscripción?", default=False)

    objects = PagesManager()
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", blank=True, null=True)

    class Meta:
        verbose_name = "actividad"
        verbose_name_plural = "actividades"
        ordering = ['dia__order', 'horaDesde', '-title']

    def __str__(self):
        return self.title

    @property
    def categoriesSTR(self):
        if self.categories is None:
            return False
        if self.categories.all() is None:
            return False
        return ', '.join(str(c) for c in self.categories.all())

    @property
    def titleSTR(self):
        return ''.join([c if c.isalnum() else " " for c in self.title])

    @property
    def modalidadSTR(self):
        return "Online" if self.modalidad else "Presencial"

    @property
    def actividadSTR(self):
        str = self.modalidadSTR + " - " + self.title
        str += " (nuevo)" if self.nuevo else ""
        return str

    @property
    def Qanotados(self):
        subscripcion = Subscription.objects.find_page(self)
        if subscripcion is None:
            return 0
        if len(subscripcion) > 0:
            return subscripcion.count()
        return 0

    @property
    def anotados(self):
        subscripcion = Subscription.objects.find_page(self)
        if subscripcion is None:
            return 0
        if len(subscripcion) > 0:
            return subscripcion
        return 0

      

    def historialHoyCreate(self):
        # Se busca la plantilla de asistencias del día correspondientes a la página
        date = datetime.now()
        return Historial.objects.find_or_create(page=self, date=date)

    def historialHoy(self):
        # Se busca la plantilla de asistencias del día correspondientes a la página
        date = datetime.now()
        historial = Historial.objects.find(page=self, date=date)
        if historial is None:
            return None
        return historial

    @property
    def asistioUltimaActividad(self, user):
        historial = Historial.objects.find_page(self)
        if historial is None:
            return None
        if len(historial) > 0:
            ultHistorial = historial.order_by('-fecha')[0]
            if user in ultHistorial.asistentes:
                return True
            return False
        return None

    @property
    def asistentes(self):
        if self.historialHoy() is None:
            return None
        return self.historialHoy().asistentes.all()

    @property
    def Qasistentes(self):
        if self.historialHoy() is None:
            return 0
        return self.historialHoy().Qasistentes

    @property
    def subscripciones(self):
        subscripcion = Subscription.objects.find_page(self)
        if subscripcion is None:
            return None
        if len(subscripcion) > 0:
            return subscripcion
        return None


class SubscriptionManager(models.Manager):
    def overlaps(self, user, page):
        subs = self.find(user)
        if subs is None:
            return False
        if subs.pages is None:
            return False
        for s in subs.pages.all():
            if s.dia == page.dia:
                if s.horaDesde is None or s.horaHasta is None or page.horaDesde is None or page.horaHasta is None:
                    return False
                sfechadesde = datetime.strptime(str(s.horaDesde), '%H:%M:%S')
                sfechahasta = datetime.strptime(str(s.horaHasta), '%H:%M:%S')
                pagefechadesde = datetime.strptime(str(page.horaDesde), '%H:%M:%S')
                pagefechahasta = datetime.strptime(str(page.horaHasta), '%H:%M:%S')

                if sfechadesde <= pagefechadesde < sfechahasta or sfechadesde < pagefechahasta <= sfechahasta:
                    return True
        return False

    def find(self, user):
        queryset = self.filter(user=user)
        if len(queryset) > 0:
            return queryset[0]
        return None

    def find_or_create(self, user):
        subscription = self.find(user=user)
        if subscription is None:
            subscription = Subscription.objects.create(user=user)
        return subscription

    def find_page(self, page):
        queryset = self.filter(pages=page)
        if len(queryset) > 0:
            return queryset
        return None


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, null=True)
    pages = models.ManyToManyField(Page, related_name='pages')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", blank=True, null=True)

    objects = SubscriptionManager()

    class Meta:
        verbose_name = "Subscripcion"
        verbose_name_plural = "Subscripciones"
        ordering = ['-updated']

    def __str__(self):
        print(self.user)
        if self.user is None:
            return 'Sin datos'
        return self.user.username



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
                                fecha__month=date.month,
                                fecha__day=date.day
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
    page = models.ForeignKey(Page, related_name="pagina", verbose_name='Actividad', null=True, on_delete=models.CASCADE)
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
        if self.asistentes.all() is None:
            return 0
        if len(self.asistentes.all()) > 0:
            return self.asistentes.count()
        return 0

    @property
    def Qanotados(self):
        return self.anotados.count()


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
    page = models.ForeignKey(Page, related_name="pagina_cuestionario_respuesta", verbose_name='Actividad', null=True, on_delete=models.CASCADE)
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
    page = models.ForeignKey(Page, related_name="pagina_cuestionario", verbose_name='Actividad', null=True, on_delete=models.CASCADE)
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
