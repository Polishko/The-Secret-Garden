from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from thesecretgarden.orders.models import Order


UserModel = get_user_model()


class OrderCancelViewTest(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@email.com'
        )

        self.client = Client()


    def login_user(self):
        self.client.login(username='testuser', password='testpass')


    def test_cancel_order__successful__redirects_updates_status_and_generates_message(self):
        self.login_user()

        order = Order.objects.create(user=self.user, status='pending')

        response = self.client.post(reverse('order-cancel', kwargs={
            'user_slug': self.user.slug,
        }))

        self.assertRedirects(response, reverse('plants-list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your order has been canceled!")

        order.refresh_from_db()
        self.assertEqual(order.status, 'canceled')
        self.assertFalse(order.is_active)


    def test_cancel_order__unauthorized_access__raises_404(self):
        another_user = UserModel.objects.create_user(
            username='anotheruser',
            password='testpass',
            email='anotheruser@email.com'
        )

        Order.objects.create(user=another_user, status='pending')

        self.login_user()
        response = self.client.post(reverse('order-cancel', kwargs={
            'user_slug': self.user.slug,
        }))

        self.assertEqual(response.status_code, 404)

    def test_cancel_order_with_validation_error(self):
        self.login_user()

        Order.objects.create(user=self.user, status='pending')

        # Mock a ValidationError during order.cancel()
        with patch('thesecretgarden.orders.models.Order.cancel', side_effect=ValidationError(["Cancellation error"])):
            response = self.client.post(reverse('order-cancel', kwargs={'user_slug': self.user.slug}))

            # Assert redirection and error message
            self.assertRedirects(response, reverse('plants-list'))
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertIn("Order could not be canceled: Cancellation error", str(messages[0]))


