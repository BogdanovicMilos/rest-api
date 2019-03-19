from django.test import TestCase


from django.contrib.auth import get_user_model
from .models import Status

User = get_user_model()


class StatusTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='milos', email='bogdanovic.milos@gmail.com')
        user.set_password('testing321')
        user.save()

    def test_creating_status(self):
        user = User.objects.get(username='milos')
        obj = Status.objects.create(user=user, content='Some cool content test')
        self.assertEqual(obj.id, 1)
        qs = Status.objects.all()
        self.assertEqual(qs.count(), 1)
