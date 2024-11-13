from unittest import TestCase

from django.contrib.auth import get_user_model

from thesecretgarden.accounts.models import Profile

UserModel = get_user_model()


class UserProfileSignalTests(TestCase):
    def test_profile_creation_signal(self):
        user = UserModel.objects.create(username='testuser', email='test@example.com',
                                        password='testpass')
        self.assertTrue(Profile.objects.filter(user=user).exists())
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.first_name,'Anonymous')
        self.assertEqual(profile.last_name,'User')
