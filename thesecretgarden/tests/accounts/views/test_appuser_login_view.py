from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class AppUserLoginViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123"
        )

    def test_login_view_with_valid_credentials(self):
        response = self.client.post(
            reverse('login'),
            data={
                'username': 'testuser',
                'password': 'securepassword123',
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('plants-list'))

        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_with_invalid_credentials(self):
        response = self.client.post(
            reverse('login'),
            data={
                'username': 'testuser',
                'password': 'wrongpassword',
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login-page.html')
        self.assertContains(response, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_view_renders_correct_template(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login-page.html')
