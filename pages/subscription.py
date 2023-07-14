from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class SubscriptionManager(models.Manager):
    def overlaps(self, user, page):
        subs = self.find(user)
        if subs is None:
            return False
        if subs.pages is None:
            return False
        if subs.pages.filter(
            fecha=page.fecha,
            horaDesde__isnull=False,
            horaHasta__isnull=False,
            horaDesde__lte=page.horaHasta,
            horaHasta__gte=page.horaDesde
        ).exists():
            return True
        else:
            return False

    def find(self, user):
        queryset = self.filter(user=user)
        if queryset.exists():
            return queryset.first()
        return None

    def find_or_create(self, user):
        subscription = self.find(user=user)
        if subscription is None:
            subscription = Subscription.objects.create(user=user)
        return subscription

    def find_page(self, page):
        queryset = self.filter(pages=page).order_by('-created')
        if len(queryset) > 0:
            return queryset
        return None


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, null=True)
    pages = models.ManyToManyField('Page', related_name='page_subscriptions')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", blank=True, null=True)

    objects = SubscriptionManager()

    class Meta:
        verbose_name = "Subscripcion"
        verbose_name_plural = "Subscripciones"
        ordering = ['-updated']

    def __str__(self):
        if self.user is None:
            return 'Sin datos'
        return self.user.username