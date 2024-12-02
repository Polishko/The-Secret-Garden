from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class MaxQuantityValidator:
    def __init__(self, max_quantity=100, message=None):
        self.max_quantity = max_quantity
        self.message = message or f'Quantity cannot exceed {self.max_quantity}.'

    def __call__(self, value):
        if value > self.max_quantity:
            raise ValidationError(self.message)

    def __eq__(self, other):
        return (
            isinstance(other, MaxQuantityValidator) and
            self.max_quantity == other.max_quantity and
            self.message == other.message
        )
