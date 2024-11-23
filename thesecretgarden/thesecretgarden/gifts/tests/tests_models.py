from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from thesecretgarden.gifts.models import Gift


class GiftModelTests(TestCase):
    def setUp(self):
        self.mock_photo = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'sample image content',
            content_type='image/jpeg'
        )

        self.gift = Gift.objects.create(
            brand_name='Katarzyna',
            short_name='Contemplations',
            short_description='Malbec & Merlot, 2023',
            type='red wine',
            price=Decimal('13.99'),
            stock=10,
            photo=self.mock_photo
        )

    def test_create_gift_with_photo(self):
        self.assertEqual(self.gift.brand_name, 'Katarzyna')
        self.assertEqual(self.gift.short_name, 'Contemplations')
        self.assertEqual(self.gift.short_description, 'Malbec & Merlot, 2023')
        self.assertEqual(self.gift.type, 'red wine')
        self.assertEqual(self.gift.slug, 'katarzyna-contemplations')
        self.assertTrue(self.gift.photo.name.startswith("images/gifts/test_image"))
        self.assertTrue(self.gift.photo.name.endswith(".jpg"))

    def test_clean_raises_validation_error_on_same_product_creation(self):
        with self.assertRaises(ValidationError) as context:
            Gift.objects.create(
                brand_name='Katarzyna',
                short_name='Contemplations',
                short_description='Malbec & Merlot, 2023',
                type='red wine',
                price=Decimal('13.99'),
                stock=10,
                photo=self.mock_photo
            )
            self.assertEqual('This product is already registered in stock!',
                             context.exception.message)

    def test_clean_raises_validation_error_on_invalid_type(self):
        self.gift.type = 'bonbons'
        with self.assertRaises(ValidationError) as context:
            self.gift.full_clean()
            self.assertIn(f'{self.gift.type} is not in listed gift type choices!',
                             context.exception.message_dict)

    def test_slug_remains_unchanged_on_short_name_change(self):
        self.gift.short_name = 'Contemplations New Series'
        self.gift.save()
        self.assertEqual(self.gift.slug, 'katarzyna-contemplations')

    def test_brand_name_correctly_capitalized(self):
        self.gift.brand_name = 'katarZyna winerY'
        self.gift.save()
        self.assertEqual(self.gift.brand_name, 'Katarzyna Winery')

    def test_short_name_correctly_capitalized(self):
        self.gift.short_name = 'conTemplations'
        self.gift.save()
        self.assertEqual(self.gift.short_name, 'Contemplations')

    def tearDown(self):
        if hasattr(self, 'gift') and self.gift.photo:
            self.gift.photo.delete(save=False)
        if hasattr(self, 'gift'):
            self.gift.delete()
