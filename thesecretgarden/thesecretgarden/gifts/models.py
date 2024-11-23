from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models

from thesecretgarden.common.models import Product

class Gift(Product):
    GIFT_CHOICES = [
        ('red wine', 'Red Wine'),
        ('chocolate', 'Chocolate'),
        ('candle', 'Candle'),
    ]

    name = None
    brand_name = Product._meta.get_field('name').clone()

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

    type = models.CharField(
        max_length=9,
        null=False,
        blank=False,
        choices=GIFT_CHOICES,
        verbose_name='Type',
        default='red wine',
        help_text='Provide gift type.'
    )

    def clean(self):
        super().clean()
        is_same_gift_in_stock = Gift.objects.filter(
            brand_name=self.brand_name,
            short_name=self.short_name,
            short_description=self.short_description,
        ).exclude(pk=self.pk).exists()

        if is_same_gift_in_stock:
            raise ValidationError('This product is already registered in stock!')

    class Meta:
        verbose_name = 'Gift'

    def __str__(self):
        return f'Gift: {self.brand_name} ({self.type})'
