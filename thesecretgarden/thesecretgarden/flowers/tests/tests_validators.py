from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from django.core.exceptions import ValidationError

from thesecretgarden.flowers.validators import PlantNameValidator, PlantDescriptionValidator, PlantPriceValidator, \
    FileSizeValidator


class PlantNameValidatorTests(TestCase):
    def setUp(self):
        self.validator = PlantNameValidator()

    def test_valid_plant_name(self):
        try:
            self.validator('Pink Roses')
        except ValidationError:
            self.fail('PlantNameValidator raised ValidationError unexpectedly!')

    def test_invalid_plant_name_1(self):
        with self.assertRaises(ValidationError) as context:
            self.validator('Pink_Roses!')

            self.assertEqual(
                context.exception.message,
                'Plant name must contain only letters or spaces!'
            )

    def test_invalid_plant_name_2(self):
        with self.assertRaises(ValidationError) as context:
            self.validator('Pinkish Amazing Cool Roses!')

            self.assertEqual(
                context.exception.message,
                'Plant name should consist of no more than 3 words!'
            )


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


class PlantPriceValidatorTests(TestCase):
    def setUp(self):
        self.validator = PlantPriceValidator()

    def test_valid_price(self):
        try:
            self.validator(Decimal(12.5567))
        except ValidationError:
            self.fail('PlantPriceValidator raised ValidationError unexpectedly!')

    def test_invalid_price_1(self):
        with self.assertRaises(ValidationError) as context:
            self.validator(0)

            self.assertEqual(
                context.exception.message,
                'Price must be a positive number!'
            )

    def test_invalid_price_2(self):
        with self.assertRaises(ValidationError):
            self.validator(-1.22)


class FileSizeValidatorTests(TestCase):
    def setUp(self):
        self.MAX_FILE_SIZE = 5
        self.validator = FileSizeValidator(self.MAX_FILE_SIZE)
        self.mock_photo = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'sample image content',
            content_type='image/jpeg'
        )

    def tearDown(self):
        if self.mock_photo:
            self.mock_photo.close()

    def test_valid_file_size(self):
        self.mock_photo.size = 5 * 1024 * 1024
        try:
            self.validator(self.mock_photo)
        except ValidationError:
            self.fail('FileSizeValidator raised ValidationError unexpectedly!')

    def test_invalid_file_size(self):
        self.mock_photo.size = 6 * 1024 * 1024
        with self.assertRaises(ValidationError) as context:
            self.validator(self.mock_photo)

            self.assertEqual(
                context.exception.message,
                f'File size must be below or equal to {self.MAX_FILE_SIZE}MB.'
            )
