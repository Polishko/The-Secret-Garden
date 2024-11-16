from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class PlantNameValidator:
    def __init__(self, field_name, message=None):
        self.field_name = field_name
        self.message = message or f'Plant name must contain only letters!'


    def __call__(self, value):
        if not value.isalpha():
            raise ValidationError(self.message)


@deconstructible
class PlantPriceValidator:
    def __init__(self, field_name):
        self.field_name = field_name

    def __call__(self, value):
        if not value.isdigit():
            raise ValidationError('Price must consist of only digits!')

        if value <= 0:
            raise ValidationError('Price must be higher than zero!')
