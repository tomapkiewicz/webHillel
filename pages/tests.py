import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Page, Historial, Subscription
import datetime


# Create your tests here.
class PageTestCase(TestCase):
    def setUp(self):
        self.page = Page.objects.create(title="Entrenamiento Funcional")

        self.user1 = User.objects.create(username='user1', password='1234')
        self.user2 = User.objects.create(username='user2', password='1234')
        self.user3 = User.objects.create(username='user3', password='1234')

    def test_add_users_to_subscription(self):
        # self.subscripcion = Subscription.objects.create(user=self.user1) Esto pinchó por metodo get de find
        self.subscripcion = Subscription.objects.find_or_create(self.user2)
        self.subscripcion.pages.add(self.page.pk)
        fecha = datetime.datetime.now() 
        self.assertEqual(self.page.Qanotados, 1)

    def test_add_users_to_historial(self):
        # self.subscripcion = Subscription.objects.create(user=self.user1) Esto pinchó por metodo get de find
        self.subscripcion = Subscription.objects.find_or_create(self.user2)
        self.subscripcion.pages.add(self.page.pk)
        fecha = datetime.datetime.now()
        self.historial = Historial.objects.create(fecha=fecha, page=self.page)
        self.historial.asistentes.add(self.user1.pk)
        self.assertEqual(self.historial.Qasistentes, 1)

    def test_add_users_to_historial_2(self):
        # self.subscripcion = Subscription.objects.create(user=self.user1) Esto pinchó por metodo get de find
        self.subscripcion = Subscription.objects.find_or_create(self.user2)
        self.subscripcion.pages.add(self.page.pk)
        fecha = datetime.datetime.now()
        self.historial = Historial.objects.create(fecha=fecha, page=self.page)
        self.historial.asistentes.add(self.user1.pk)
        self.subscribers = Subscription.objects.find_page(self.page)
        self.qsuscribers = self.subscribers.count()
        self.assertEqual(self.historial.Qasistentes, self.qsuscribers)

    def test_add_users_to_historial_3(self):
        # self.subscripcion = Subscription.objects.create(user=self.user1) Esto pinchó por metodo get de find
        self.subscripcion = Subscription.objects.find_or_create(self.user2)
        self.subscripcion.pages.add(self.page.pk)
        fecha = datetime.datetime.now()
        self.historial = Historial.objects.create(fecha=fecha, page=self.page)
        self.historial.asistentes.add(self.user1.pk)
        self.subscribers = Subscription.objects.find_page(self.page)
        self.Qasistentes = self.page.asistentes.count()
        self.assertEqual(self.historial.Qasistentes, self.Qasistentes)