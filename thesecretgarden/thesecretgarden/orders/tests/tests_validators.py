from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from thesecretgarden.common.validators import ProductPriceValidator


class OrderPriceValidatorTests(TestCase):
    def setUp(self):
        # Validator with custom range for orders
        self.validator = ProductPriceValidator(min_value=0, max_value=999999.99)

    def test_valid_total_price(self):
        try:
            self.validator(Decimal(123456.78))  # Valid for orders
        except ValidationError:
            self.fail('Order price validator raised ValidationError unexpectedly!')

    def test_invalid_total_price_exceeding_max(self):
        with self.assertRaises(ValidationError) as context:
            self.validator(Decimal(1000000))  # Exceeds max_value for orders

        self.assertEqual(
            context.exception.message,
            'Maximum price is 999999.99!'  # Custom max_value message for orders
        )
