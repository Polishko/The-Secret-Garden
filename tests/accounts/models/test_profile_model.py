from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from thesecretgarden.accounts.models import Profile

UserModel = get_user_model()

class AppUserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
        }

    def test_create_user_with_valid_data(self):
        user = UserModel.objects.create_user(**self.user_data)
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.role, 'customer')
        self.assertEqual(user.slug, self.user_data['username'])

    def test_create_user_with_duplicate_username(self):
        UserModel.objects.create_user(**self.user_data)
        with self.assertRaises(ValidationError):
            UserModel.objects.create_user(
                username='testuser',
                email='newemail@example.com',
                password='testpass123'
            )

    def test_create_user_with_duplicate_email(self):
        UserModel.objects.create_user(**self.user_data)
        with self.assertRaises(ValidationError):
            UserModel.objects.create_user(
                username='newuser',
                email='test@example.com',
                password='testpass123'
            )

    def tearDown(self):
        UserModel.objects.all().delete()


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
            self.fail('Clean method raised ValidationError unexpectedly!')

    def test_clean_method_for_address_field(self):
        profile = Profile.objects.get(user=self.user)
        profile.address = ' 123 Amazing <script>console.log("Hi!")</script> St.  '

        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_name_formatting_on_save(self):
        profile = Profile.objects.get(user=self.user)
        profile.first_name = '  JOHN '
        profile.last_name = 'doE  '
        profile.save()
        self.assertEqual(profile.first_name, 'John')
        self.assertEqual(profile.last_name, 'Doe')

    def tearDown(self):
        UserModel.objects.all().delete()
