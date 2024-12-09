from datetime import date, timedelta

from django.core.exceptions import ValidationError
from thesecretgarden.accounts.validators import NameValidator, PhoneNumberValidator, \
    AddressValidator, BirthdayValidator
from django.test import TestCase


class ProfileNameValidatorTests(TestCase):
    def setUp(self):
        self.validator = NameValidator(field_name='first name')

    def test_valid_name(self):
        try:
            self.validator('validname')
        except ValidationError:
            self.fail('NameValidator raised ValidationError unexpectedly!')

    def test_invalid_name(self):
        with self.assertRaises(ValidationError):
            self.validator('invalid3user@name!')


class PhoneNumberValidatorTests(TestCase):
    def setUp(self):
        self.validator = PhoneNumberValidator()

    def test_valid_phone_number(self):
        try:
            self.validator('0893451289')
        except ValidationError:
            self.fail('PhoneNumberValidator raised ValidationError unexpectedly!')

    def test_invalid_phone_number_1(self):
        with self.assertRaises(ValidationError):
            self.validator('8934512890')

    def test_invalid_phone_number_2(self):
        with self.assertRaises(ValidationError):
            self.validator('089345128')

    def test_invalid_phone_number_3(self):
        with self.assertRaises(ValidationError):
            self.validator('088934512!')


class AddressValidatorTests(TestCase):
    def setUp(self):
        self.validator = AddressValidator()

    def test_valid_address(self):
        try:
            self.validator('Amazing 123 Street')
        except ValidationError:
            self.fail('AddressValidator raised ValidationError unexpectedly!')

    def test_invalid_address(self):
        with self.assertRaises(ValidationError):
            self.validator('Amazing 123 <script>console.log(Hi!)</scrit>')


class BirthdayValidatorTests(TestCase):
    def setUp(self):
        self.validator = BirthdayValidator()

    def test_valid_birthday(self):
        try:
            self.validator(date(2000, 12, 12))
        except ValidationError:
            self.fail('BirthdateValidator raised ValidationError unexpectedly!')

    def test_invalid_birthday_1(self):
        with self.assertRaises(ValidationError):
            self.validator(date(1889, 12, 12))

    def test_invalid_birthday_2(self):
        future_date = date.today() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.validator(future_date)
