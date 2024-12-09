import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


# Product validators
@deconstructible
class ProductNameValidator:
    def __init__(self, valid_characters=None, valid_length=None):
        self.valid_characters = valid_characters or "Product name must contain only letters or spaces!"
        self.valid_length = valid_length or "Product name should consist of no more than 3 words!"

    def __call__(self, value):
        if not re.fullmatch(r'[a-zA-Z\s]+', value):
            raise ValidationError(self.valid_characters)

        if len(value.split()) > 3:
            raise ValidationError(self.valid_length)


@deconstructible
class ProductPriceValidator:
    def __init__(self, min_value_message=None, max_value_message=None):
        self.min_value_message = min_value_message or "Price must be a greater than 0!"
        self.max_value_message = max_value_message or "Maximum price is 999.99!"

    def __call__(self, value):
        if value <= 0:
            raise ValidationError(self.min_value_message)

        if value > 999.99:
            raise ValidationError(self.max_value_message)


@deconstructible
class ProductStockValidator:
    def __init__(self, message=None):
        self.message = message or "Max stock capacity is 100!"

    def __call__(self, value):
        if value > 100:
            raise ValidationError(self.message)

# Contact message validators
@deconstructible
class ContactNameValidator:
    def __init__(self, message=None):
        self.valid_characters = message or "Your name must contain only letters or spaces!"

    def __call__(self, value):
        if not re.fullmatch(r'^[a-zA-Z\s]+$', value):
            raise ValidationError(self.valid_characters)


@deconstructible
class ContactMessageValidator:
    def __init__(self, valid_characters=None, valid_length=None):
        self.message = valid_characters or "Message cannot contain invalid characters like < or >."
        self.valid_length = valid_length or "Message should not exceed 1000 characters!"

    def __call__(self, value):
        if re.search(r'[<>]', value):
            raise ValidationError(self.message)
