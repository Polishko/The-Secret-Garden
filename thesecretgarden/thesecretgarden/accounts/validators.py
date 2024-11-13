from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator:
    def __init__(self, message=None):
        self.message = message or 'Username must contain only letters and numbers!'


    def __call__(self, value):
        if not value.isalnum():
            raise ValidationError(self.message)
