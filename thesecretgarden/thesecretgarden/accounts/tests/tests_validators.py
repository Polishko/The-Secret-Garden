from django.core.exceptions import ValidationError
from thesecretgarden.accounts.validators import UsernameValidator, NameValidator
from django.test import TestCase


class UsernameValidatorTests(TestCase):
    def setUp(self):
        self.validator = UsernameValidator()

    def test_valid_username(self):
        try:
            self.validator('ValidUsername123')
        except ValidationError:
            self.fail("UsernameValidator raised ValidationError unexpectedly!")

    def test_invalid_username(self):
        with self.assertRaises(ValidationError):
            self.validator('invalid@Username!')


class ProfileNameValidatorTests(TestCase):
    def setUp(self):
        self.validator = NameValidator(field_name='first name')

    def test_valid_name(self):
        try:
            self.validator('validname')
        except ValidationError:
            self.fail("NameValidator raised ValidationError unexpectedly!")

    def test_invalid_name(self):
        with self.assertRaises(ValidationError):
            self.validator('invalid3user@name!')
