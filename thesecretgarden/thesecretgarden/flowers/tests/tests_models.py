from decimal import Decimal
from unittest import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile

from thesecretgarden.flowers.models import Plant


class PlantModelTests(TestCase):
    def setUp(self):
        self.mock_photo = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'sample image content',
            content_type='image/jpeg'
        )

        self.plant = Plant.objects.create(
            name='Roses',
            type='floral',
            description='A simple and elegant rose bouquet prepared with our best roses.',
            price=Decimal('10.99'),
            stock=50,
            photo=self.mock_photo
        )

    def test_create_plant_with_photo(self):
        self.assertEqual(self.plant.name, 'Roses')
        self.assertEqual(self.plant.type, 'floral')
        self.assertTrue(self.plant.photo.name.startswith("images/flowers/test_image"))
        self.assertTrue(self.plant.photo.name.endswith(".jpg"))

    def tearDown(self):
        if hasattr(self, 'plant') and self.plant.photo:
            self.plant.photo.delete(save=False)
        if hasattr(self, 'plant'):
            self.plant.delete()

