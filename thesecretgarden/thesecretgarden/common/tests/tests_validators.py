from decimal import Decimal

# from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from django.core.exceptions import ValidationError

from thesecretgarden.common.validators import (
    ProductNameValidator,
    ProductPriceValidator, ProductStockValidator
)


class ProductNameValidatorTests(TestCase):
    def setUp(self):
        self.validator = ProductNameValidator()

    def test_valid_product_name(self):
        try:
            self.validator('Test product')
        except ValidationError:
            self.fail('PlantNameValidator raised ValidationError unexpectedly!')

    def test_invalid_product_name_1(self):
        with self.assertRaises(ValidationError) as context:
            self.validator('Test_Product!')

            self.assertEqual(
                context.exception.message,
                'Product name must contain only letters or spaces!'
            )

    def test_invalid_product_name_2(self):
        with self.assertRaises(ValidationError) as context:
            self.validator('Such a Cool wonderful product')

            self.assertEqual(
                context.exception.message,
                'Plant name should consist of no more than 3 words!'
            )


class ProductPriceValidatorTests(TestCase):
    def setUp(self):
        self.validator = ProductPriceValidator()

    def test_valid_price(self):
        try:
            self.validator(Decimal(12.56))
        except ValidationError:
            self.fail('ProductPriceValidator raised ValidationError unexpectedly!')

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

    def test_invalid_price_3(self):
        with self.assertRaises(ValidationError):
            self.validator(1000)


class ProductStockValidatorTests(TestCase):
    def setUp(self):
        self.validator = ProductStockValidator()

    def test_valid_stock(self):
        try:
            self.validator(100)
        except ValidationError:
            self.fail('ProductStockValidator raised ValidationError unexpectedly!')

    def test_invalid_stock_1(self):
        with self.assertRaises(ValidationError):
            self.validator(101)


# class FileSizeValidatorTests(TestCase):
#     def setUp(self):
#         self.MAX_FILE_SIZE = 5
#         self.validator = FileSizeValidator(self.MAX_FILE_SIZE)
#         self.mock_photo = SimpleUploadedFile(
#             name='test_image.jpg',
#             content=b'sample image content',
#             content_type='image/jpeg'
#         )
#
#     def tearDown(self):
#         if self.mock_photo:
#             self.mock_photo.close()
#
#     def test_valid_file_size(self):
#         self.mock_photo.size = 5 * 1024 * 1024
#         try:
#             self.validator(self.mock_photo)
#         except ValidationError:
#             self.fail('FileSizeValidator raised ValidationError unexpectedly!')
#
#     def test_invalid_file_size(self):
#         self.mock_photo.size = 6 * 1024 * 1024
#         with self.assertRaises(ValidationError) as context:
#             self.validator(self.mock_photo)
#
#             self.assertEqual(
#                 context.exception.message,
#                 f'File size must be below or equal to {self.MAX_FILE_SIZE}MB.'
#             )
