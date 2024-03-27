from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

class RegistrationTest(TestCase):
    def test_registration_view(self):

        data = {
            'login': 'testuser',
            'email': 'testuser@example.com',
            'pass1': 'testpassword',
            'pass2': 'testpassword',
        }

        response = self.client.post(reverse('register'), data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertRedirects(response, reverse('auth'))

