from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.fields import BooleanField
from datetime import datetime, timedelta
import pytz
from location.models import Provincia
from .category import Category
from .responsable import Responsable
from .colaborador import Colaborador
from .subscription import Subscription
from .historial import Historial


def custom_upload_to(instance, filename):
    old_instance = Page.objects.select_related().filter(pk=instance.pk).first()
    if old_instance is not None:
        old_instance.flyer.delete()
    return "pages/" + filename


class RecurrentPage(models.Model):
    DIAS_CHOICES = [
        ("monday", "Lunes"),
        ("tuesday", "Martes"),
        ("wednesday", "Miércoles"),
        ("thursday", "Jueves"),
        ("friday", "Viernes"),
        ("saturday", "Sábado"),
        ("sunday", "Domingo"),
    ]

    title = models.CharField(verbose_name="Título", max_length=200)
    horaDesde = models.TimeField(verbose_name="Hora desde", null=True, blank=True)
    horaHasta = models.TimeField(verbose_name="Hora hasta", null=True, blank=True)
    description = RichTextField(verbose_name="Descripción", null=True, blank=True)
    textoExtraMail = RichTextField(
        verbose_name="Texto extra del mail", null=True, blank=True
    )
    con_mail_personalizado = BooleanField(
        verbose_name="Con mail personalizado", default=False
    )
    asunto_mail = models.CharField(
        verbose_name="Asunto del mail", max_length=200, null=True, blank=True
    )
    cuerpo_mail = RichTextField(verbose_name="Cuerpo del mail", null=True, blank=True)
    flyer = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    fechaDesde = models.DateField(verbose_name="Fecha desde", null=True, blank=True)
    fechaHasta = models.DateField(verbose_name="Fecha hasta", null=True, blank=True)
    cupo = models.SmallIntegerField(verbose_name="Cupo", default=0)
    modalidad = BooleanField(verbose_name="Online", default=False)
    nuevo = BooleanField(verbose_name="Nuevo", default=False)
    activa = BooleanField(verbose_name="Activa", default=True)
    oculta = BooleanField(verbose_name="Oculta", default=False)
    categories = models.ManyToManyField(
        Category,
        verbose_name="Categorias",
        related_name="get_recurrent_pages",
        blank=True,
    )
    provincia = models.ForeignKey(
        Provincia, on_delete=models.CASCADE, null=True, blank=True
    )
    dias = models.CharField(verbose_name="Días", max_length=100)
    responsable = models.ForeignKey(
        Responsable, on_delete=models.CASCADE, null=True, blank=True
    )
    colaborador = models.ForeignKey(
        Colaborador, on_delete=models.CASCADE, null=True, blank=True
    )
    secreta = BooleanField(verbose_name="Tiene clave?", default=False)
    clave = models.CharField(
        verbose_name="Clave", null=True, blank=True, default="", max_length=200
    )
    con_preinscripcion = BooleanField(
        verbose_name="Tiene preinscripción?", default=False
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación", blank=True, null=True
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de edición", blank=True, null=True
    )
    pages = models.ManyToManyField(
        "Page", verbose_name="Actividades", related_name="get_pages", blank=True
    )

    class Meta:
        verbose_name = "Actividad recurrente"
        verbose_name_plural = "Actividades recurrentes"
        ordering = ["fechaDesde"]

    def __str__(self):
        return self.title

    def create_pages(self):
        # Calculate the list of dates based on the start and end dates and the selected days
        dates = self.calculate_dates()

        # Iterate over the dates and create a Page object for each date
        for date in dates:
            page = Page(
                title=self.title,
                horaDesde=self.horaDesde,
                horaHasta=self.horaHasta,
                description=self.description,
                textoExtraMail=self.textoExtraMail,
                con_mail_personalizado=self.con_mail_personalizado,
                asunto_mail=self.asunto_mail,
                cuerpo_mail=self.cuerpo_mail,
                flyer=self.flyer,
                fecha=date,
                cupo=self.cupo,
                modalidad=self.modalidad,
                nuevo=self.nuevo,
                activa=self.activa,
                oculta=self.oculta,
                provincia=self.provincia,
                responsable=self.responsable,
                colaborador=self.colaborador,
                secreta=self.secreta,
                clave=self.clave,
                con_preinscripcion=self.con_preinscripcion,
                recurrent_page=self,
            )
            page.save()
            page.categories.set(self.categories.all())
            self.pages.add(page)

    def calculate_dates(self):
        # Create a dictionary mapping lowercase English day names to Spanish day names
        spanish_days = {
            "monday": "lunes",
            "tuesday": "martes",
            "wednesday": "miércoles",
            "thursday": "jueves",
            "friday": "viernes",
            "saturday": "sábado",
            "sunday": "domingo",
        }

        # Convert the selected days to lowercase English names
        selected_days = [day[0] for day in self.DIAS_CHOICES if day[0] in self.dias]

        # Calculate the list of dates based on the start and end dates and the selected days
        dates = []
        date = self.fechaDesde
        while date <= self.fechaHasta:
            if date.strftime("%A").lower() in selected_days:
                dates.append(date)
            date += timedelta(days=1)
        return dates

    @property
    def actividadSTR(self):
        str = self.modalidadSTR + " - " + self.title
        str += " (nuevo)" if self.nuevo else ""
        return str

    @property
    def modalidadSTR(self):
        return "Online" if self.modalidad else "Presencial"

    def save(self, *args, **kwargs):
        is_new_instance = not self.pk  # Check if it's a new instance
        super().save(*args, **kwargs)

        if is_new_instance:
            self.create_pages()


class Page(models.Model):
    title = models.CharField(verbose_name="Título", max_length=200)

    alerta = models.TextField(verbose_name="Alerta", null=True, blank=True)

    horaDesde = models.TimeField(
        verbose_name="Hora desde",
        null=True,
        blank=True,
        auto_now=False,
        auto_now_add=False,
    )
    horaHasta = models.TimeField(
        verbose_name="Hora hasta",
        null=True,
        blank=True,
        auto_now=False,
        auto_now_add=False,
    )
    description = RichTextField(verbose_name="Descripción", null=True, blank=True)
    textoExtraMail = RichTextField(
        verbose_name="Texto extra del mail", null=True, blank=True
    )
    con_mail_personalizado = BooleanField(
        verbose_name="Tiene mail personalizado?", default=False
    )
    asunto_mail = models.CharField(
        verbose_name="Asunto del mail",
        null=True,
        blank=True,
        default="",
        max_length=200,
    )
    cuerpo_mail = RichTextField(verbose_name="Cuerpo del mail", null=True, blank=True)

    flyer = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    fecha = models.DateField(verbose_name="Fecha", null=True, blank=True)
    cupo = models.SmallIntegerField(verbose_name="Cupo", default=0)
    modalidad = BooleanField(verbose_name="Online", default=False)
    nuevo = BooleanField(verbose_name="Nuevo", default=False)
    activa = BooleanField(verbose_name="Activa", default=True)
    oculta = BooleanField(verbose_name="Oculta", default=False)
    categories = models.ManyToManyField(
        Category, verbose_name="categorias", related_name="get_pages", blank=True
    )

    provincia = models.ForeignKey(
        Provincia, on_delete=models.CASCADE, null=True, blank=True
    )
    responsable = models.ForeignKey(
        Responsable, on_delete=models.CASCADE, null=True, blank=True
    )
    colaborador = models.ForeignKey(
        Colaborador, on_delete=models.CASCADE, null=True, blank=True
    )

    secreta = BooleanField(verbose_name="Tiene clave?", default=False)
    clave = models.CharField(
        verbose_name="Clave", null=True, blank=True, default="", max_length=200
    )
    con_preinscripcion = BooleanField(
        verbose_name="Tiene preinscripción?", default=False
    )
    cowork = models.BooleanField(verbose_name="Es para el Cowork?", default=False)
    cowork_day_title = models.CharField(
        verbose_name="Título del día para el cowork", max_length=200, blank=True
    )

    # objects = PagesManager()
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación", blank=True, null=True
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de edición", blank=True, null=True
    )

    recurrent_page = models.ForeignKey(
        RecurrentPage,
        on_delete=models.CASCADE,
        related_query_name="page",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "actividad"
        verbose_name_plural = "actividades"
        ordering = ["horaDesde", "-title"]

    def __str__(self):
        return self.title

    @property
    def categoriesSTR(self):
        if self.categories is None:
            return False
        categories = self.categories.values_list("name", flat=True)
        if not categories.exists():
            return False
        return ", ".join(categories)

    @property
    def titleSTR(self):
        return "".join([c if c.isalnum() else " " for c in self.title])

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
    def Qconfirmados(self):
        if not self.con_preinscripcion:
            return self.Qanotados
        return Subscription.objects.filter(pages_confirmadas=self).count()

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
        local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
        date = datetime.now(local_tz)
        return Historial.objects.find_or_create(page=self, date=date)

    def historialHoy(self):
        # Se busca la plantilla de asistencias del día correspondientes a la página
        local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
        date = datetime.now(local_tz)
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
            ultHistorial = historial.order_by("-fecha")[0]
            if user in ultHistorial.asistentes:
                return True
            return False
        return None

    @property
    def asistentes(self):
        historial = self.historialHoy()
        if historial is None:
            return None
        return historial.asistentes.all()

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
