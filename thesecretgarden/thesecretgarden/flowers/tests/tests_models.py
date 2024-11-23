from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from thesecretgarden.flowers.models import Plant


class PlantModelTests(TestCase):
    def setUp(self):
        self.mock_photo = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'sample image content',
            content_type='image/jpeg'
        )

        self.plant = Plant.objects.create(
            name='Pink Roses',
            type='floral',
            description='A simple and elegant rose bouquet prepared with our best roses.',
            price=Decimal('10.99'),
            stock=50,
            photo=self.mock_photo
        )

    def test_create_plant_with_photo(self):
        self.assertEqual(self.plant.name, 'Pink Roses')
        self.assertEqual(self.plant.type, 'floral')
        self.assertEqual(self.plant.slug, 'pink-roses')
        self.assertTrue(self.plant.photo.name.startswith("images/flowers/test_image"))
        self.assertTrue(self.plant.photo.name.endswith(".jpg"))

    def test_clean_raises_validation_error_on_invalid_type(self):
        self.plant.type = 'bonbons'
        with self.assertRaises(ValidationError) as context:
            self.plant.full_clean()
            self.assertIn(f'{self.plant.type} is not in listed gift type choices!',
                             context.exception.message_dict)

    def test_type_max_length_constraint_applied(self):
        with self.assertRaises(ValidationError):
            self.plant.type = 'Green house plant'
            self.plant.save()


    def tearDown(self):
        if hasattr(self, 'plant') and self.plant.photo:
            self.plant.photo.delete(save=False)
        if hasattr(self, 'plant'):
            self.plant.delete()
