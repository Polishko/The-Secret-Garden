from django.test import TestCase

from thesecretgarden.accounts.models import AppUser


class AppUserManagerTests(TestCase):
    def test_create_user(self):
        user = AppUser.objects.create_user(username='testuser', email='testuser@example.com',
                                           password='password123')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')

        self.assertTrue(user.check_password('password123'))

    def test_create_superuser(self):
        admin_user = AppUser.objects.create_superuser(username='adminuser', email='adminuser@example.com',
                                                      password='adminpassword')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.username, 'adminuser')
        self.assertEqual(admin_user.email, 'adminuser@example.com')