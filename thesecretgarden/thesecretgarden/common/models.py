from decimal import Decimal

from cloudinary.models import CloudinaryField
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from django.db import models
from django.utils.text import slugify

from thesecretgarden.common.validators import ProductNameValidator, ProductPriceValidator, ProductStockValidator
from thesecretgarden.orders.models import OrderItem


class Product(models.Model):
    # MAX_FILE_SIZE = 5

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

    photo = CloudinaryField(
        'image',
        null=False,
        blank=False,
        help_text='Upload an image for the product.',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


    def get_available_stock(self):
        """
        Provides stock snapshot based on currently placed orders and stock status.
        """
        product_content_type = ContentType.objects.get_for_model(self)

        reserved_stock = sum(
            item.quantity for item in OrderItem.objects.filter(
                content_type=product_content_type,
                object_id=self.pk,
                order__status='pending'
            )
        )

        return self.stock - reserved_stock

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
        if hasattr(self, 'name') and self.name:
            self.name = self.clean_name_field(self.name)

        if hasattr(self, 'brand_name') and self.brand_name:
            self.brand_name = self.clean_name_field(self.brand_name)

        if hasattr(self, 'short_name') and self.short_name:
            self.short_name = self.clean_name_field(self.short_name)

        if hasattr(self, 'short_description') and self.short_description:
            self.short_description = self.clean_name_field(self.short_description)

        if not self.slug:
            if hasattr(self, 'name') and self.name:
                self.slug = slugify(self.name.lower())

            elif hasattr(self, 'brand_name') and hasattr(self, 'short_name'):
                gift_name_to_slugify = f"{self.brand_name or ''} {self.short_name or ''}".strip()
                self.slug = slugify(gift_name_to_slugify.lower())

        if self.price and not isinstance(self.price, Decimal):
            self.price = Decimal(self.price).quantize(Decimal('0.01'))

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
