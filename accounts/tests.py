from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.slug, 'testuser')
        self.assertEqual(str(self.profile), 'testuser')

    def test_profile_view(self):
        url = reverse('accounts:profile', kwargs={'slug': self.profile.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_profile_edit(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('accounts:edit_profile', kwargs={'slug': self.profile.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {'bio': 'This is a test bio.'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.bio, 'This is a test bio.')


class SignUpViewTestCase(TestCase):
    def test_signup_view(self):
        url = reverse('accounts:signup')
        data = {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)