from django.db import models
import datetime
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToManyField
from django.db.models.fields.related_descriptors import ManyToManyDescriptor
from django.dispatch import receiver
from django.db.models.signals import post_save
from pages.models import Category, Subscription
from location.models import Provincia
from itertools import groupby
from django.db.models import Q


def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return "profiles/" + filename


class FechaTaglit(models.Model):
    fecha = models.CharField(verbose_name="Fecha", max_length=200)
    order = models.SmallIntegerField(verbose_name="Orden")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación", blank=True, null=True
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de edición", blank=True, null=True
    )

    class Meta:
        verbose_name = "FechaTaglit"
        verbose_name_plural = "FechasTaglit"
        ordering = ["order"]

    def __str__(self):
        return self.fecha


class FechaOnward(models.Model):
    fecha = models.CharField(verbose_name="Fecha", max_length=200)
    order = models.SmallIntegerField(verbose_name="Orden", default=0)
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación", blank=True, null=True
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de edición", blank=True, null=True
    )

    class Meta:
        verbose_name = "FechaOnward"
        verbose_name_plural = "FechasOnward"
        ordering = ["order"]

    def __str__(self):
        return self.fecha


class TemporadaOnward(models.Model):
    temporada = models.BooleanField(verbose_name="En temporada")
    updated = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de modificación"
    )
    created = models.DateTimeField(auto_now=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "TemporadaOnward"
        verbose_name_plural = "TemporadaOnward"
        ordering = ["temporada"]

    def __str__(self):
        return "Temporada: Activa" if self.temporada else "Temporada: Inactiva"


class RandomOrderManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("?")


class PropuestaInteres(models.Model):
    nombre = models.CharField(verbose_name="Propuesta", max_length=200)
    order = models.SmallIntegerField(verbose_name="Orden", default=0)
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación", blank=True, null=True
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de edición", blank=True, null=True
    )
    objects = RandomOrderManager()

    class Meta:
        verbose_name = "PropuestaInteres"
        verbose_name_plural = "PropuestasInteres"

    def __str__(self):
        return self.nombre


class TematicaInteres(models.Model):
    nombre = models.CharField(verbose_name="Tematica", max_length=200)
    order = models.SmallIntegerField(verbose_name="Orden", default=0)
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación", blank=True, null=True
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de edición", blank=True, null=True
    )
    objects = RandomOrderManager()

    class Meta:
        verbose_name = "TematicaInteres"
        verbose_name_plural = "TematicasInteres"

    def __str__(self):
        return self.nombre


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # ,related_name='get_user_profile'
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    perfil_ok = models.CharField(null=True, blank=True, max_length=999)
    observaciones = models.CharField(null=True, blank=True, max_length=999)
    apellido = models.CharField(null=True, blank=True, max_length=100)
    nombre = models.CharField(null=True, blank=True, max_length=100)
    whatsapp = models.CharField(
        verbose_name="Número de Whatsapp", null=True, blank=True, max_length=30
    )
    instagram = models.CharField(
        verbose_name="@ de Instagram", null=True, blank=True, max_length=100
    )
    onward = models.ForeignKey(
        FechaOnward,
        on_delete=models.CASCADE,
        verbose_name="¿Viajaste o vas a viajar a Onward? ¿Cuándo?",
        null=True,
        blank=True,
    )
    taglit = models.ForeignKey(
        FechaTaglit,
        on_delete=models.CASCADE,
        verbose_name="¿Viajaste o vas a viajar a Taglit? ¿Cuándo?",
        null=True,
        blank=True,
    )
    propuestasInteres = models.ManyToManyField(PropuestaInteres)
    tematicasInteres = models.ManyToManyField(TematicaInteres)
    comoConociste = models.CharField(
        verbose_name="¿Cómo conociste Hillel?", null=True, blank=True, max_length=250
    )
    estudios = models.CharField(
        verbose_name="¿Estás estudiando, o te recibiste? ¿Qué estudias/te y en qué institución?",
        null=True,
        blank=True,
        max_length=250,
    )
    experienciaComunitaria = models.CharField(null=True, blank=True, max_length=250)
    fechaNacimiento = models.DateField(null=True, blank=True)
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.CASCADE,
        verbose_name="provincia",
        null=True,
        blank=True,
    )
    categories = models.ManyToManyField(
        Category, verbose_name="Intereses", related_name="get_user_pages", blank=True
    )
    validado = models.BooleanField(verbose_name="Perfil validado", default=0)
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación", blank=True, null=True
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de edición", blank=True, null=True
    )
    email_verificado = models.BooleanField(
        default=False, verbose_name="Email verificado"
    )

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
        ordering = ["-updated"]

    def __str__(self):
        return self.user.username

    @property
    def subscription(self):
        subscription = Subscription.objects.find(self.user)
        if subscription is None:
            return
        if subscription.pages is None:
            return
        return subscription.pages.all()

    @property
    def active_subscription(self):
        subscription = Subscription.objects.find(self.user)
        if not subscription:
            return []

        recurrent_pages = []
        non_recurrent_pages = []

        # ✅ Include pages with no date too
        for page in subscription.pages.filter(activa=True).filter(Q(fecha__gte=date.today()) | Q(fecha__isnull=True)):
            if page.recurrent_page:
                recurrent_pages.append(page)
            else:
                non_recurrent_pages.append(page)

        # Group recurrent pages by recurrent_page field
        grouped_recurrent_pages = []
        for _, group in groupby(recurrent_pages, key=lambda p: p.recurrent_page):
            group = list(group)
            first_page = group[0]
            grouped_recurrent_pages.append(first_page)

        # Combine recurrent and non-recurrent pages, sorted by fecha
        combined_pages = grouped_recurrent_pages + non_recurrent_pages
        sorted_pages = sorted(combined_pages, key=lambda p: p.fecha or date.max)

        return sorted_pages

    @property
    def edad(self):
        if self.fechaNacimiento is None:
            return
        today = date.today()
        return (
            today.year
            - self.fechaNacimiento.year
            - (
                (today.month, today.day)
                < (self.fechaNacimiento.month, self.fechaNacimiento.day)
            )
        )

    @property
    def interesesSTR(self):
        if not self.categories.exists():
            return False
        return ", ".join(str(c) for c in self.categories.all())

    @property
    def tematicasInteresSTR(self):
        if not self.tematicasInteres.exists():
            return False
        return ", ".join(str(c) for c in self.tematicasInteres.all())

    @property
    def propuestasInteresSTR(self):
        if not self.propuestasInteres.exists():
            return False
        return ", ".join(str(c) for c in self.propuestasInteres.all())

    def save(self, *args, **kwargs):
        if not self.pk and self.user_id:
            # Check if a profile already exists for the user before creating a new one
            existing_profile = Profile.objects.filter(user=self.user)
            if existing_profile.exists():
                return  # Don't create a new profile if one already exists
        if self.fechaNacimiento is not None:
            if self.fechaNacimiento > datetime.date.today():
                raise ValidationError(
                    "La fecha de nacimiento no puede ser una fecha futura!"
                )
        super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get("created", False):
        Profile.objects.get_or_create(user=instance)
        # print("Se acaba de crear un usuario y su perfil enlazado")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
