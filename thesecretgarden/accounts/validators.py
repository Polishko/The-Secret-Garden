import re
from datetime import date

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator:
    def __init__(self, message=None):
        self.message = message or 'Username must contain only letters and numbers!'


    def __call__(self, value):
        if not value.isalnum():
            raise ValidationError(self.message)


@deconstructible
class NameValidator:
    def __init__(self, field_name, message=None):
        self.field_name = field_name
        self.message = message or f'Your {self.field_name} must contain only letters!'


    def __call__(self, value):
        if not value.isalpha():
            raise ValidationError(self.message)


@deconstructible
class PhoneNumberValidator:
    def __init__(self, message=None):
        self.message = message or 'Enter a valid phone number of 10 digits!'

    def __call__(self, value):
        if not re.match(r'^0\d{9}$', value):
            raise ValidationError(self.message)


@deconstructible
class AddressValidator:
    def __init__(self, message=None):
        self.message = message or 'Invalid address.'

    def __call__(self, value):
        if re.search(r'[<>]', value):
            raise ValidationError(self.message)


@deconstructible
class BirthdayValidator:
    def __init__(self, min_year=1900, future_error=None, past_error=None):
        self.min_year = min_year
        self.future_error = future_error or 'Birthday cannot be after today!'
        self.past_error = past_error or f'Birthday cannot be before {min_year}!'

    def __call__(self, value):
        if value > date.today():
            raise ValidationError(self.future_error)
        if value.year < self.min_year:
            raise ValidationError(self.past_error)
