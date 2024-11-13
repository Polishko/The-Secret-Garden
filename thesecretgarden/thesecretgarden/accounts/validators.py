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
