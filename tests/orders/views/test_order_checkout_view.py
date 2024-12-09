from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import get_messages
from thesecretgarden.orders.models import Order, OrderItem
from thesecretgarden.flowers.models import Plant

UserModel = get_user_model()


class OrderCheckOutViewTest(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@test.com'
        )

        self.client.login(username='testuser', password='testpass')

        self.plant = Plant.objects.create(
            name="Test Plant",
            price=20.00,
            stock=10,
            type='floral',
            photo='plant.jpg',
            description='Some cool plant'
        )


    def test_checkout__with_no_pending_order__redirects_and_shows_error(self):
        response = self.client.get(reverse('order-checkout', kwargs={
            'user_slug': self.user.slug,
        }))

        self.assertRedirects(response, reverse('shopping-cart', kwargs={
            'user_slug': self.user.slug,
        }))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Order not found or unauthorized access.")


    def test_checkout__with_valid_order__shows_correct_content(self):
        order = Order.objects.create(user=self.user, status='pending', total_price=0)

        OrderItem.objects.create(
            order=order,
            content_type=ContentType.objects.get_for_model(self.plant),
            object_id=self.plant.pk,
            quantity=2,
            price_per_unit=self.plant.price,
        )

        response = self.client.get(reverse('order-checkout', kwargs={
            'user_slug': self.user.slug,
        }))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order-checkout.html')

        self.assertEqual(response.context['order_sum'], 40.00)


    def test_order_with_incorrect_total_price__on_checkout__updated_correctly(self):
        order = Order.objects.create(user=self.user, status='pending', total_price=10)

        OrderItem.objects.create(
            order=order,
            content_type=ContentType.objects.get_for_model(self.plant),
            object_id=self.plant.pk,
            quantity=2,
            price_per_unit=self.plant.price,
        )

        response = self.client.get(reverse('order-checkout', kwargs={
            'user_slug': self.user.slug,
        }))

        order.refresh_from_db()
        self.assertEqual(order.total_price, 40.00)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order-checkout.html')
        self.assertEqual(response.context['order_sum'], 40.00)


    def test_checkout_with_calculation_error(self):
        order = Order.objects.create(user=self.user, status='pending', total_price=0)

        # Mock calculate_total to raise an exception
        with patch.object(Order, 'calculate_total', side_effect=Exception("Calculation failed")):
            response = self.client.get(reverse('order-checkout', kwargs={
            'user_slug': self.user.slug,
        }))

            self.assertRedirects(response, reverse('shopping-cart', kwargs={
            'user_slug': self.user.slug,
        }))

            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertIn("An error occurred while calculating your order", str(messages[0]))
