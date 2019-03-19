from django.test import TestCase


from django.contrib.auth import get_user_model

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='milos', email='bogdanovic.milos@gmail.com')
        user.set_password('testing321')
        user.save()

    def test_created_user(self):
        qs = User.objects.filter(username='milos')
        self.assertEqual(qs.count(), 1)
