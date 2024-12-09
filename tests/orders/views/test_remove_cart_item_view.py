from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, Client
from django.urls import reverse
from thesecretgarden.orders.models import Order, OrderItem
from thesecretgarden.flowers.models import Plant
from thesecretgarden.gifts.models import Gift


UserModel = get_user_model()


class RemoveCartItemViewTest(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@email.com'
        )

        self.plant = Plant.objects.create(
            name="Test Plant",
            price=20.00,
            stock=10,
            type='floral',
            photo='plant.jpg',
            description='I am a green plant'
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

    def login_user(self):
        self.client.login(username='testuser', password='testpass')


    def test_remove_cart_item__removes_items_successfully(self):
        self.login_user()

        order = Order.objects.create(user=self.user, status='pending')
        order_item = OrderItem.objects.create(
            order=order,
            content_type=ContentType.objects.get_for_model(self.plant),
            object_id=self.plant.pk,
            quantity=2,
            price_per_unit=self.plant.price,
        )

        response = self.client.post(reverse('remove-item', kwargs={
            'user_slug': self.user.slug,
            'item_id': order_item.id
        }))

        self.assertRedirects(response, reverse('shopping-cart', kwargs={
            'user_slug': self.user.slug,
        }))
        self.assertFalse(OrderItem.objects.filter(id=order_item.id).exists())


    def test_remove_cart_item__nonexistent_item__shows_error(self):
        self.login_user()

        response = self.client.post(reverse('remove-item', kwargs={
            'user_slug': self.user.slug,
            'item_id': 0
        }))

        self.assertRedirects(response, reverse('shopping-cart', kwargs={
            'user_slug': self.user.slug,
        }))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Item not found or unauthorized access.")

    def test_remove_cart_item__unauthorized_access__does_not_allow_deleting(self):
        other_user = UserModel.objects.create_user(
            username='otheruser',
            password='otherpass',
            email='otheruser@test.com'
        )

        order = Order.objects.create(user=other_user, status='pending')

        order_item = OrderItem.objects.create(
            order=order,
            content_type=ContentType.objects.get_for_model(self.plant),
            object_id=self.plant.pk,
            quantity=2,
            price_per_unit=self.plant.price,
        )

        self.login_user()

        response = self.client.post(reverse('remove-item', kwargs={
            'user_slug': self.user.slug,
            'item_id': order_item.id
        }))

        self.assertRedirects(response, reverse('shopping-cart', kwargs={
            'user_slug': self.user.slug,
        }))
        self.assertTrue(OrderItem.objects.filter(id=order_item.id).exists())
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Item not found or unauthorized access.")
