from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, Client
from django.urls import reverse
from thesecretgarden.orders.models import Order, OrderItem
from thesecretgarden.flowers.models import Plant
from thesecretgarden.gifts.models import Gift

UserModel = get_user_model()

class CartViewTest(TestCase):

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

    def test_cart_view_with_pending_order__shows_correct_content(self):
        self.login_user()
        order = Order.objects.create(user=self.user, status='pending')

        OrderItem.objects.create(
            order=order,
            content_type=ContentType.objects.get_for_model(self.plant),
            object_id=self.plant.pk,
            quantity=2,
            price_per_unit=self.plant.price,
        )

        OrderItem.objects.create(
            order=order,
            content_type=ContentType.objects.get_for_model(self.gift),
            object_id=self.gift.pk,
            quantity=1,
            price_per_unit=self.gift.price,
        )

        response = self.client.get(reverse('shopping-cart', kwargs={
            'user_slug': self.user.slug,
        }))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/shopping-cart.html')

        context = response.context
        self.assertIsNotNone(context['order'])
        self.assertEqual(len(context['order_items']), 2)
        self.assertEqual(context['total_cost'], 70.00)


    def test_cart_view_without_pending_order__shows_correct_content(self):
        self.login_user()

        response = self.client.get(reverse('shopping-cart', kwargs={
            'user_slug': self.user.slug,
        }))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/shopping-cart.html')

        context = response.context
        self.assertIsNone(context['order'])
        self.assertEqual(context['order_items'], [])
        self.assertEqual(context['total_cost'], 0)


    def test_cart_view__unauthenticated_user__redirects_to_login(self):
        response = self.client.get(reverse('shopping-cart', kwargs={
            'user_slug': self.user.slug,
        }))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('shopping-cart', kwargs={
            'user_slug': self.user.slug,
        })}")


    def test_cart_view_handles_attribute_error(self):
        self.login_user()
        order = Order.objects.create(user=self.user, status='pending')

        OrderItem.objects.create(
            order=order,
            content_type=ContentType.objects.get_for_model(self.plant),
            object_id=self.plant.pk,
            quantity=2,
            price_per_unit=self.plant.price,
        )

        self.plant.delete()

        response = self.client.get(reverse('shopping-cart', kwargs={
            'user_slug': self.user.slug,
        }))

        self.assertRedirects(response, reverse('plants-list'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "An error occurred while loading your cart.")
