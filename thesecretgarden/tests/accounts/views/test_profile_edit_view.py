from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ProfileEditViewTests(TestCase):
    def setUp(self):
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

        self.valid_data = {
            'first_name': 'UpdatedFirstName',
            'last_name': 'UpdatedLastName',
            'address': 'Updated address.',
        }

    def test_access_denied_for_unauthenticated_users(self):
        self.client.logout()
        response = self.client.get(reverse('profile-edit', kwargs={'slug': self.user.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/accounts/{self.user.slug}/edit/')

    def test_access_denied_for_non_owners(self):
        response = self.client.get(reverse('profile-edit', kwargs={'slug': self.other_user.slug}))
        self.assertEqual(response.status_code, 403)

    def test_successful_profile_update(self):
        response = self.client.post(
            reverse('profile-edit', kwargs={'slug': self.user.slug}),
            data=self.valid_data
        )
        self.profile.refresh_from_db()

        self.assertEqual(self.profile.first_name, 'Updatedfirstname')
        self.assertEqual(self.profile.last_name, 'Updatedlastname')
        self.assertEqual(self.profile.address, 'Updated address.')

        self.assertRedirects(response, reverse('profile-details', kwargs={'slug': self.user.slug}))
