from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from thesecretgarden.flowers.models import Plant

User = get_user_model()

class AddToCartViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com"
        )

        self.client.login(username="testuser", password="testpassword")

        self.plant = Plant.objects.create(
            name="Test Plant",
            stock=10,
            price=5.00,
            description="A lovely test plant.",
        )

    def tearDown(self):
        """
        Clean up resources after each test case.
        """
        User.objects.all().delete()
        Plant.objects.all().delete()

    def test_add_to_cart_url(self):
        response = self.client.post(reverse('add-to-cart', args=('plant', self.plant.id)), {'quantity': 1})
        self.assertEqual(response.status_code, 302)  # Redirect
