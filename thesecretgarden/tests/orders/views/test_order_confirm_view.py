from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from thesecretgarden.orders.models import Order, OrderItem
from thesecretgarden.flowers.models import Plant
from thesecretgarden.gifts.models import Gift

UserModel = get_user_model()

class OrderConfirmViewTest(TestCase):

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

    def test_confirm_order__with_no_pending_order__redirects_and_shows_error(self):
        self.login_user()

        response = self.client.post(reverse('order-confirm'))

        self.assertRedirects(response, reverse('shopping-cart'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Order not found or unauthorized access.")


    def test_confirm_order__without_address__redirects_to_profile_edit(self):
        self.login_user()
        Order.objects.create(user=self.user, status='pending')

        self.user.profile.address = ''
        self.user.profile.save()

        response = self.client.post(reverse('order-confirm'))

        self.assertRedirects(response, reverse('profile-edit', kwargs={'slug': self.user.slug}))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You must provide an address to place an order.")


    def test_confirm_order__successfully_completes_order(self):
        self.login_user()
        profile = self.user.profile
        profile.address = "Test Address"
        profile.save()

        order = Order.objects.create(user=self.user, status='pending')

        OrderItem.objects.create(
            order=order,
            content_type=ContentType.objects.get_for_model(self.plant),
            object_id=self.plant.pk,
            quantity=1,
            price_per_unit=self.plant.price,
        )

        response = self.client.post(reverse('order-confirm'))

        order.refresh_from_db()
        self.assertEqual(order.status, 'completed')

        self.assertRedirects(response, reverse('completed-orders'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your order has been successfully completed!")
