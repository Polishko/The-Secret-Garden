from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase


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
