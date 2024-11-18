from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class GiftPriceValidator:
    def __init__(self, message=None):
        self.message = message or 'Price must be a greater than 0!'

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
