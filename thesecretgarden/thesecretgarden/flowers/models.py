from decimal import Decimal

from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.utils.html import strip_tags
from django.utils.text import slugify

from thesecretgarden.flowers.validators import PlantNameValidator, PlantPriceValidator, \
    FileSizeValidator, PlantDescriptionValidator


class Plant(models.Model):
    PLANT_CHOICES = [
        ('non-floral', 'Non Floral Plants'),
        ('floral', 'Floral Plants'),
        ('cactus', 'Cactuses'),
    ]

    MAX_FILE_SIZE = 5

    name = models.CharField(
        null=False,
        blank=False,
        max_length=100,
        unique=True,
        validators=(
            PlantNameValidator(),
        ),
        verbose_name='Type',
        help_text='Enter plant name (up to 3 words).'
    )

    slug = models.SlugField(
        unique=True,
        editable=False,
        null=True,
        blank=True,
    )

    type = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        choices=PLANT_CHOICES,
        verbose_name='Type',
        help_text='Provide plant type.'
    )

    description = models.TextField(
        null=False,
        blank=False,
        validators=(
            PlantDescriptionValidator(),
            MinLengthValidator(10, message='Description should be at least 10 characters.'),
            MaxLengthValidator(300, message='Description should not exceed 1000 characters.'),
        ),
        verbose_name='Description',
        help_text = 'Provide a description for the plant product.'
    )

    price = models.DecimalField(
        null=False,
        blank=False,
        validators=(
            PlantPriceValidator(),
        ),
        decimal_places=2,
        max_digits=6,
        verbose_name='Price',
        help_text='Provide plant price.'
    )

    stock = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name='Stock',
        help_text='Provide stock amount.'
    )

    photo = models.ImageField(
        upload_to='images/flowers',
        validators=(
            FileSizeValidator(MAX_FILE_SIZE),
        ),
        null=False,
        blank=False,
    )

    def save(self, *args, **kwargs):
        if self.description:
            self.description = ' '.join(strip_tags(self.description).split())

        if self.name:
            self.name = ' '.join(word.capitalize() for word in self.name.split())

        if not self.slug:
            self.slug = slugify(self.name.lower())

        if self.price and not isinstance(self.price, Decimal):
            self.price = Decimal(self.price).quantize(Decimal('0.01'))

        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Plant'
        ordering = ['name']

    def __str__(self):
        return f'Plant: {self.name} ({self.type})'
