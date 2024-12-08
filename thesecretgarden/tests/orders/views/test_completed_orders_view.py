from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from thesecretgarden.orders.models import Order

UserModel = get_user_model()


class CompletedOrdersViewTest(TestCase):
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

        self.completed_order_1 = Order.objects.create(user=self.user, status='completed', is_active=False)
        self.completed_order_2 = Order.objects.create(user=self.user, status='completed', is_active=False)
        self.another_user_order = Order.objects.create(user=self.another_user, status='completed', is_active=False)

    def login_user(self):
        self.client.login(username='testuser', password='testpass')

    def test_completed_orders_view__user_logged_in__displays_completed_orders_for_logged_in_user(self):
        self.login_user()

        completed_order = Order.objects.create(user=self.user, status='completed', is_active=False)

        print("Created Order ID:", completed_order.pk)

        response = self.client.get(reverse('completed-orders', kwargs={'user_slug': self.user.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/orders-list.html')

        orders = response.context['orders']
        self.assertEqual(len(orders), 3)
        self.assertIn(completed_order, orders)

    def test_completed_orders_view__no_orders__displays_empty_(self):
        self.login_user()

        Order.objects.filter(user=self.user).delete()

        response = self.client.get(reverse('completed-orders', kwargs={
            'user_slug': self.user.slug
        }))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/orders-list.html')

        orders = response.context['orders']
        self.assertEqual(len(orders), 0)

        self.assertContains(response, 'completed orders')

    def test_completed_orders_view__unauthenticated_user__is_redirected(self):
        response = self.client.get(reverse('completed-orders', kwargs={
            'user_slug': self.user.slug
        }))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))
