from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify

from thesecretgarden.gifts.validators import GiftPriceValidator, FileSizeValidator


class Gift(models.Model):
    GIFT_CHOICES = [
        ('red wine', 'Red Wine'),
        ('chocolate', 'Chocolate'),
        ('candle', 'Candle'),
    ]

    MAX_FILE_SIZE = 5

    brand_name = models.CharField(
        null=False,
        blank=False,
        max_length=50,
        validators=(
            MinLengthValidator(3),
        ),
        verbose_name='Brand Name',
        help_text='Enter the brand name.',
    )

    short_name = models.CharField(
        null=False,
        blank=False,
        max_length=50,
        verbose_name='Short Name',
        help_text='Enter the product short name.',
    )

    short_description = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        validators=(
            MinLengthValidator(5),
        ),
        verbose_name='Short Description',
        help_text='Enter short product description.',
    )

    slug = models.SlugField(
        unique=True,
        editable=False,
        verbose_name='Slug',
    )

    type = models.CharField(
        max_length=9,
        null=False,
        blank=False,
        choices=GIFT_CHOICES,
        verbose_name='Type',
        default='red wine',
        help_text='Provide gift type.'
    )

    price = models.DecimalField(
        null=False,
        blank=False,
        validators=(
            GiftPriceValidator(),
        ),
        decimal_places=2,
        max_digits=7,
        verbose_name='Price',
        help_text='Provide gift price.'
    )

    stock = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name='Stock',
        help_text='Provide stock amount.'
    )

    photo = models.ImageField(
        upload_to='images/gifts',
        validators=(
            FileSizeValidator(MAX_FILE_SIZE),
        ),
        null=False,
        blank=False,
    )

    def clean(self):
        super().clean()
        valid_types = [gift_type[0] for gift_type in self.GIFT_CHOICES]

        if self.type not in valid_types:
            raise ValidationError(f'{self.type} is not in listed gift type choices!')

        is_same_gift_in_stock = Gift.objects.filter(
            brand_name=self.brand_name,
            short_name=self.short_name,
            short_description=self.short_description,
        ).exclude(pk=self.pk).exists()

        if is_same_gift_in_stock:
            raise ValidationError('This product is already registered in stock!')

    def save(self, *args, **kwargs):
        if self.brand_name:
            self.brand_name = ' '.join(word.title() for word in self.brand_name.split())

        if self.short_name:
            self.short_name = ' '.join(word.title() for word in self.short_name.split())

        if self.short_description:
            self.short_description = ' '.join(word.title() for word in self.short_description.split())

        if not self.slug:
            self.slug = slugify(f'{self.brand_name.lower()} {self.short_name.lower()}')

        if self.price and not isinstance(self.price, Decimal):
            self.price = Decimal(self.price).quantize(Decimal('0.01'))

        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Gift'
        ordering = ['brand_name']

    def __str__(self):
        return f'Gift: {self.brand_name} ({self.type})'
