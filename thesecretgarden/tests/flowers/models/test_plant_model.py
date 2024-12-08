from unittest.mock import patch
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from decimal import Decimal
from thesecretgarden.flowers.models import Plant


class PlantModelTests(TestCase):
    def setUp(self):
        self.mock_photo = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'sample image content',
            content_type='image/jpeg'
        )

    @patch('thesecretgarden.flowers.models.upload')
    def test_create_plant__valid_data__creates_plant(self, mock_upload):
        mock_upload.return_value = {'public_id': 'mocked_public_id'}

        plant = Plant.objects.create(
            name='Pink Roses',
            type='floral',
            description='A simple and elegant rose bouquet prepared with our best roses.',
            price=Decimal('10.99'),
            stock=50,
            photo=self.mock_photo
        )

        self.assertEqual(plant.name, 'Pink Roses')
        self.assertEqual(plant.type, 'floral')
        self.assertEqual(plant.slug, 'pink-roses')
        self.assertEqual(str(plant.photo), 'mocked_public_id')


    @patch('thesecretgarden.flowers.models.upload')
    def test_clean__on_invalid_type__raises_validation_error(self, mock_upload):
        mock_upload.return_value = {'public_id': 'mocked_public_id'}

        plant = Plant.objects.create(
            name='Pink Roses',
            type='floral',
            description='A simple and elegant rose bouquet prepared with our best roses.',
            price=Decimal('10.99'),
            stock=50,
            photo=self.mock_photo
        )

        plant.type = 'bonbons'
        with self.assertRaises(ValidationError) as context:
            plant.full_clean()

        self.assertIn("Value 'bonbons' is not a valid choice.", str(context.exception))

    @patch('thesecretgarden.flowers.models.upload')
    def test_type_max_length_constraint_applied(self, mock_upload):
        mock_upload.return_value = {'public_id': 'mocked_public_id'}

        plant = Plant.objects.create(
            name='Pink Roses',
            type='floral',
            description='A simple and elegant rose bouquet prepared with our best roses.',
            price=Decimal('10.99'),
            stock=50,
            photo=self.mock_photo
        )

        plant.type = 'Green house plant'
        with self.assertRaises(ValidationError):
            plant.save()
