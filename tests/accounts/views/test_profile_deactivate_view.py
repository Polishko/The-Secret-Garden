from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ProfileDeactivateViewTests(TestCase):
    def setUp(self):
        # Create two users and their profiles
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@example.com'
        )
        self.profile = self.user.profile

        self.other_user = UserModel.objects.create_user(
            username='otheruser',
            password='testpass',
            email='otheruser@example.com'
        )
        self.other_profile = self.other_user.profile

        self.client.login(username='testuser', password='testpass')

    def test_access_denied_for_unauthenticated_users(self):
        self.client.logout()
        response = self.client.get(reverse('profile-deactivate', kwargs={'slug': self.user.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/accounts/{self.user.slug}/deactivate/')

    def test_access_denied_for_non_owners(self):
        response = self.client.get(reverse('profile-deactivate', kwargs={'slug': self.other_user.slug}))
        self.assertEqual(response.status_code, 403)

    def test_profile_deactivate_confirmation_page(self):
        response = self.client.get(reverse('profile-deactivate', kwargs={'slug': self.user.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile-deactivate-confirm.html')
        self.assertContains(response, 'Are you sure you want to deactivate your profile?')

    def test_successful_profile_deactivation(self):
        response = self.client.post(reverse('profile-deactivate', kwargs={'slug': self.user.slug}))
        self.profile.refresh_from_db()

        self.assertFalse(self.profile.is_active)
        self.assertRedirects(response, reverse('login'))
