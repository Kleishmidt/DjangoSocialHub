from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UsersAppTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_register_view(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_profile_view(self):
        url = reverse('profile', args=[self.user.profile.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        url = reverse('profile', args=[self.user.profile.id])
        data = {
            'bio': 'New bio',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_profile_update_invalid_form(self):
        url = reverse('profile', args=[self.user.profile.id])
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

        form = response.context['p_form']
        self.assertFalse(form.is_valid())
