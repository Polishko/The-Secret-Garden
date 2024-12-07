from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from thesecretgarden.flowers.models import Plant
from thesecretgarden.gifts.models import Gift
from thesecretgarden.orders.models import Order, OrderItem

UserModel = get_user_model()


class AddToCartViewTest(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpass',
            email='testemail@test.com'
        )

        self.plant = Plant.objects.create(
            name='Test Plant',
            price=20.00,
            stock=10,
            type='floral',
            photo='plant.jpg',
            description='A pink colored nice flower'
        )

        self.gift = Gift.objects.create(
            brand_name="Test Brand",
            short_name="Test Gift",
            short_description="A short description",
            price=30.00,
            stock=5,
            type='red wine',
            photo='gift.jpg',
        )

        self.client = Client()

    def test__add_to_cart__adds_plant_to_cart_for_logged_user(self):
        self.client.login(username='testuser', password='testpass')

        response = self.client.post(reverse('add-to-cart', kwargs={
            'product_type': 'plant',
            'product_id': self.plant.pk
        }), data={'quantity': 2})

        self.assertEqual(response.status_code, 302)

        order = Order.objects.get(user=self.user, status='pending')
        order_item = OrderItem.objects.get(order=order, object_id=self.plant.pk)

        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price_per_unit, self.plant.price)
        self.assertEqual(order_item.total_price, 2 * self.plant.price)
        self.assertEqual(order_item.current_stock, self.plant.stock)


    def test__add_to_cart__adds_gift_to_cart_for_logged_user(self):
        self.client.login(username='testuser', password='testpass')

        response = self.client.post(reverse('add-to-cart', kwargs={
            'product_type': 'gift',
            'product_id': self.gift.pk
        }), data={'quantity': 3})

        self.assertEqual(response.status_code, 302)

        order = Order.objects.get(user=self.user, status='pending')
        order_item = OrderItem.objects.get(order=order, object_id=self.gift.pk)

        self.assertEqual(order_item.quantity, 3)
        self.assertEqual(order_item.price_per_unit, self.gift.price)
        self.assertEqual(order_item.total_price, 3 * self.gift.price)
        self.assertEqual(order_item.current_stock, self.gift.stock)


    def test__add_to_cart_with_insufficient_stock__does_not_create_order_for_logged_user(self):
        self.client.login(username='testuser', password='testpass')

        response = self.client.post(reverse('add-to-cart', kwargs={
            'product_type': 'plant',
            'product_id': self.plant.pk
        }), data={'quantity': 15})

        self.assertEqual(response.status_code, 302)

        order = Order.objects.filter(user=self.user, status='pending').first()
        self.assertIsNone(order)

        self.plant.refresh_from_db()
        self.assertEqual(self.plant.stock, 10)

