from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from thesecretgarden.gifts.models import Gift


class GiftFormTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'brand_name': 'Luxury Gift',
            'short_name': 'Lux',
            'type': 'red wine',
            'photo': SimpleUploadedFile("gift.jpg", b"dummy_image_data"),
            'price': Decimal('25.50'),
            'stock': 10,
            'short_description': 'An elegant luxury gift for special occasions.',
        }

    @patch('thesecretgarden.gifts.models.upload')
    def test_gift_form_valid_data_creates_gift(self, mock_upload):
        mock_upload.return_value = {'public_id': 'mocked_public_id'}
        gift = Gift.objects.create(**self.valid_data)
        self.assertEqual(gift.brand_name, 'Luxury Gift')
        self.assertEqual(gift.short_name, 'Lux')
        self.assertEqual(gift.type, 'red wine')
        self.assertEqual(gift.photo.public_id, 'mocked_public_id')

    @patch('thesecretgarden.gifts.models.upload')
    def test_gift_form_duplicate_brand_name_raises_error(self, mock_upload):
        mock_upload.return_value = {'public_id': 'mocked_public_id'}
        Gift.objects.create(**self.valid_data)
        with self.assertRaises(ValidationError):
            duplicate_data = self.valid_data.copy()
            Gift.objects.create(**duplicate_data)

    @patch('thesecretgarden.gifts.models.upload')
    def test_gift_form_invalid_type_raises_error(self, mock_upload):
        mock_upload.return_value = {'public_id': 'mocked_public_id'}
        invalid_data = self.valid_data.copy()
        invalid_data['type'] = 'invalid_type'
        with self.assertRaises(ValidationError):
            Gift.objects.create(**invalid_data)

    @patch('thesecretgarden.gifts.models.upload')
    def test_gift_delete_form_readonly_fields(self, mock_upload):
        mock_upload.return_value = {'public_id': 'mocked_public_id'}
        gift = Gift.objects.create(**self.valid_data)
        self.assertEqual(gift.photo.public_id, 'mocked_public_id')
