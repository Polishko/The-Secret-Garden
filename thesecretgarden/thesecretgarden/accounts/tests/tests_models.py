from unittest import TestCase

from django.core.exceptions import ValidationError

from thesecretgarden.accounts.models import UserModel, Profile


class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username='testuser', email='textuser@example.com',
                                                  password='testpass')

    def test_clean_method_with_same_names(self):
        profile = Profile.objects.get(user=self.user)
        profile.first_name = 'Jane'
        profile.last_name = 'Jane'

        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_clean_method_with_different_names(self):
        profile = Profile.objects.get(user=self.user)
        profile.first_name = 'Jane'
        profile.last_name = 'Doe'

        try:
            profile.full_clean()
        except ValidationError:
            self.fail("clean method raised ValidationError unexpectedly!")

    def tearDown(self):
        self.user.delete()
