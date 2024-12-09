from django.core.exceptions import ValidationError
from thesecretgarden.accounts.validators import UsernameValidator
from django.test import TestCase


class UsernameValidatorTests(TestCase):
    def setUp(self):
        self.validator = UsernameValidator()

    def test_valid_username(self):
        try:
            self.validator('ValidUsername123')
        except ValidationError:
            self.fail('UsernameValidator raised ValidationError unexpectedly!')

    def test_invalid_username(self):
        with self.assertRaises(ValidationError):
            self.validator('invalid@Username!')
