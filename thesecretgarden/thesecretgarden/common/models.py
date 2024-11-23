from decimal import Decimal
from django.core.exceptions import ValidationError

from django.db import models
from django.utils.text import slugify

from thesecretgarden.common.validators import ProductNameValidator, ProductPriceValidator, ProductStockValidator, \
    FileSizeValidator
from thesecretgarden.common.utils import dynamic_upload_to


class Product(models.Model):
    MAX_FILE_SIZE = 5

    name = models.CharField(
        null=False,
        blank=False,
        max_length=50,
        unique=True,
        validators=(
            ProductNameValidator(),
        ),
        verbose_name='Product Name',
        help_text='Enter product name (up to 3 words).',
    )

    slug = models.SlugField(
        unique=True,
        editable=False,
        verbose_name='Slug',
    )

    price = models.DecimalField(
        null=False,
        blank=False,
        validators=(
            ProductPriceValidator(),
        ),
        decimal_places=2,
        max_digits=5,
        verbose_name='Price',
        help_text='Provide product price.'
    )

    stock = models.PositiveIntegerField(
        null=False,
        blank=False,
        validators=(
            ProductStockValidator(),
        ),
        verbose_name='Stock',
        help_text='Provide stock amount.'
    )

    type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Type',
        help_text='Specify the product type.',
    )

    photo = models.ImageField(
        upload_to=dynamic_upload_to,
        null=False,
        blank=False,
        validators=[FileSizeValidator(MAX_FILE_SIZE)],
        help_text='Upload an image for the product.',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['created_at']

    def clean_name_field(self, field_value):
        if field_value:
            return ' '.join(word.title() for word in field_value.split())
        return field_value

    def clean(self):
        super().clean()
        if hasattr(self, 'TYPE_CHOICES') and self.type:
            valid_types = [choice[0] for choice in self.TYPE_CHOICES]
            if self.type not in valid_types:
                raise ValidationError({'type': f'{self.type} is not a valid type.'})

    def save(self, *args, **kwargs):
        if self.name:
            self.name = ' '.join(word.title() for word in self.name.split())

        if not self.slug:
            self.slug = slugify(self.name.lower())

        if self.price and not isinstance(self.price, Decimal):
            self.price = Decimal(self.price).quantize(Decimal('0.01'))

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
