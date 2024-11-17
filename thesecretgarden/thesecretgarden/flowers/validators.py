import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class PlantNameValidator:
    def __init__(self, valid_characters=None, valid_length=None):
        self.valid_characters = valid_characters or 'Plant name must contain only letters or spaces!'
        self.valid_length = valid_length or 'Plant name consist of no more than 3 words!'

    def __call__(self, value):
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise ValidationError(self.valid_characters)

        if len(value.split()) > 3:
            raise ValidationError(self.valid_length)
        

@deconstructible
class PlantDescriptionValidator:
    def __init__(self, message=None):
        self.message = message or 'Description contains invalid characters.'

    def __call__(self, value):
        if re.search(r'[<>]', value):
            raise ValidationError(self.message)


@deconstructible
class PlantPriceValidator:
    def __init__(self, message=None):
        self.message = message or 'Price must be a positive number!'

    def __call__(self, value):
        if value <= 0:
            raise ValidationError(self.message)


@deconstructible
class FileSizeValidator:
    def __init__(self, file_size_mb, message=None):
        self.file_size_mb = file_size_mb
        self.message = message or f'File size must be below or equal to {self.file_size_mb}MB.'

    def __call__(self, value):
        if value.size > self.file_size_mb * 1024 * 1024:
            raise ValidationError(self.message)
