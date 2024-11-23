from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from thesecretgarden.common.models import Product

class ProductModelTests(TestCase):
    def setUp(self):
        self.mock_photo = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'sample image content',
            content_type='image/jpeg'
        )
        self.product = Product(
            name='Test Product',
            price=Decimal('10.99'),
            stock=50,
            photo=self.mock_photo
        )

    def test_slug_remains_unchanged_on_name_change(self):
        self.product.name = 'Test product'
        self.product.save()
        self.assertEqual(self.product.slug, 'test-product')

    def test_name_correctly_capitalized(self):
        self.product.name = 'test Product'
        self.product.save()
        self.assertEqual(self.product.name, 'Test Product')

    def test_tags_in_description_removed(self):
        self.product.description = 'An amazing present for <script>console.log(Hello there!)</script>.'
        self.product.save()
        self.assertEqual(self.product.description, 'An amazing present for console.log(Hello there!).')

    def test_duplicate_name_not_allowed(self):
        with self.assertRaises(ValidationError) as context:
            Product.objects.create(
                name='Test product',
                type='floral',
                description='Another test product.',
                price=Decimal('12.99'),
                stock=5,
                photo=self.mock_photo
            )

        self.assertIn('name', context.exception.message_dict)
        self.assertIn('slug', context.exception.message_dict)

    def test_price_max_digits_constraint_applied(self):
        with self.assertRaises(ValidationError):
            Product.objects.create(
                name='Test product',
                type='floral',
                description='Amazing blue hues.',
                price=Decimal('13.99589'),
                stock=15,
                photo=self.mock_photo
            )
