from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from thesecretgarden.orders.models import Order, OrderItem
from thesecretgarden.flowers.models import Plant
from django.contrib.contenttypes.models import ContentType

UserModel = get_user_model()


class CompletedOrderDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@email.com'
        )
        self.another_user = UserModel.objects.create_user(
            username='anotheruser',
            password='testpass',
            email='anotheruser@email.com'
        )

        self.completed_order = Order.objects.create(user=self.user, status='completed', is_active=False)
        self.another_user_order = Order.objects.create(user=self.another_user, status='completed', is_active=False)

        self.plant = Plant.objects.create(
            name="Rose",
            price=5.00,
            description='I am a green plant',
            stock=10,
        )

        plant_content_type = ContentType.objects.get_for_model(Plant)
        OrderItem.objects.create(
            order=self.completed_order,
            product=self.plant,
            quantity=2,
            price_per_unit=5.00,
            total_price=10.00,
            content_type=plant_content_type,
        )

    def login_user(self):
        self.client.login(username='testuser', password='testpass')

    def test_completed_order_detail_view__valid_user__shows_correct_view(self):
        self.login_user()
        response = self.client.get(reverse('completed-order-detail', kwargs={
            'user_slug': self.user.slug,
            'pk': self.completed_order.pk
        }))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/completed-order-detail.html')

        order = response.context['order']
        order_items = response.context['order_items']
        self.assertEqual(order, self.completed_order)
        self.assertEqual(len(order_items), 1)

        item = order_items[0]
        self.assertEqual(item['product'], self.plant)
        self.assertEqual(item['quantity'], 2)
        self.assertEqual(item['price_per_unit'], 5.00)
        self.assertEqual(item['total_price'], 10.00)
        self.assertEqual(item['product_type'], 'plant')

    def test_completed_order_detail_view__access_another_users_order__not_shown(self):
        self.login_user()
        response = self.client.get(reverse('completed-order-detail', kwargs={
            'user_slug': self.user.slug,
            'pk': self.another_user_order.pk
        }))
        self.assertEqual(response.status_code, 404)

    def test_completed_order_detail_view__nonexistent_order__not_shown(self):
        self.login_user()
        response = self.client.get(reverse('completed-order-detail', kwargs={
            'user_slug': self.user.slug,
            'pk': 999
        }))
        self.assertEqual(response.status_code, 404)

    def test_completed_order_detail_view__unauthenticated_user__redirects_to_login(self):
        response = self.client.get(reverse('completed-order-detail', kwargs={
            'user_slug': self.user.slug,
            'pk': self.completed_order.pk
        }))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_completed_order_detail_view__incorrect_status__shows_not_found(self):
        # Change the order status to something other than 'completed'
        self.completed_order.status = 'processing'
        self.completed_order.save()

        self.login_user()
        response = self.client.get(reverse('completed-order-detail', kwargs={
            'user_slug': self.user.slug,
            'pk': self.completed_order.pk
        }))
        self.assertEqual(response.status_code, 404)

    def test_completed_order_detail_view__inactive_order__shows_not_found(self):
        self.completed_order.is_active = True
        self.completed_order.save()

        self.login_user()
        response = self.client.get(reverse('completed-order-detail', kwargs={
            'user_slug': self.user.slug,
            'pk': self.completed_order.pk
        }))
        self.assertEqual(response.status_code, 404)
