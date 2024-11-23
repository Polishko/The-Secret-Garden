from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from django.core.exceptions import ValidationError

from thesecretgarden.flowers.validators import PlantDescriptionValidator


class PlantDescriptionValidatorTests(TestCase):
    def setUp(self):
        self.validator = PlantDescriptionValidator()

    def test_valid_description(self):
        try:
            self.validator('Amazing elegant pink bouquet.')
        except ValidationError:
            self.fail('PlantDescriptionValidator raised ValidationError unexpectedly!')

    def test_invalid_description_1(self):
        with self.assertRaises(ValidationError) as context:
            self.validator('Pinkish Amazing <script>console.log("Oh Hi!"))</script> Cool Roses!')

            self.assertEqual(
                context.exception.message,
                'Description cannot contain invalid characters like < or >.'
            )
