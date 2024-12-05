import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

# Deprecated - No longer used in active models
@deconstructible
class PlantDescriptionValidator:
    def __init__(self, message=None):
        self.message = message or 'Description cannot contain invalid characters like < or >.'

    def __call__(self, value):
        if re.search(r'[<>]', value):
            raise ValidationError(self.message)
