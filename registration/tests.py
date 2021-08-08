from django.test import TestCase
from .models import Profile
from pages.models import Subscription, Page
from django.contrib.auth.models import User


# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('test', 'test@test.com', 'test1234')

    def test_profile_exists(self):
        exists = Profile.objects.filter(user__username='test').exists()
        self.assertEqual(exists, True)


class newSubscriptionTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('test1', 'test@test.com', 'test1234')
        user = User.objects.filter(username='test1').first()
        subscription = Subscription.objects.find_or_create(user)

    def test_something(self):
        print("testing..")
        ss = Subscription.objects.all()
        for s in ss:
            print(s.user)
        exists = Subscription.objects.filter(user__username='test1').exists()
        self.assertEqual(exists, True)


class contadorTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('test3', 'test@test.com', 'test1234')

    def test_anotados(self):
        User.objects.create_user('test1', 'test@test.com', 'test1234')
        user = User.objects.filter(username='test1').first()
        User.objects.create_user('test2', 'test@test.com', 'test1234')
        user2 = User.objects.filter(username='test2').first()
        subscription = Subscription.objects.find_or_create(user)
        subscription2 = Subscription.objects.find_or_create(user2)

        page = Page.objects.create(title="entrenamiento funcional")
        page2 = Page.objects.create(title="coworking")
        subscription.pages.add(page)
        subscription.pages.add(page2)
        subscription2.pages.add(page)
        # self.assertEqual(Page.objects.find(page).count(), 2)
        self.assertEqual(page.Qanotados, 2)
