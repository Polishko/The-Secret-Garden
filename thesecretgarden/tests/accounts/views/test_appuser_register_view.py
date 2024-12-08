from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class AppUserRegisterViewTests(TestCase):
    def setUp(self):
        self.valid_user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        }
        self.invalid_user_data = {
            'username': '',
            'email': 'invalidemail',
            'password1': 'pass',
            'password2': 'pass123',
        }

    def test_register_view_with_valid_data(self):
        response = self.client.post(
            reverse('register'),
            data=self.valid_user_data
        )

        self.assertTrue(UserModel.objects.filter(username='newuser').exists())

        user = UserModel.objects.get(username='newuser')
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user, user)

        profile = user.profile
        if profile.is_complete():
            self.assertRedirects(response, reverse('plants-list'))
        else:
            self.assertRedirects(response, reverse('profile-edit', kwargs={'slug': user.slug}))

    def test_register_view_with_invalid_data(self):
        response = self.client.post(
            reverse('register'),
            data=self.invalid_user_data
        )

        self.assertFalse(UserModel.objects.filter(email='invalidemail').exists())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register-page.html')
        self.assertContains(response, 'This field is required')

    def test_register_view_renders_correct_template(self):
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register-page.html')
