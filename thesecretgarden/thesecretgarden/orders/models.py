from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models, transaction

from thesecretgarden.orders.validators import MaxQuantityValidator

UserModel = get_user_model()

class Order(models.Model):
    """
    Represents the overarching transaction.
    It ties the user to their purchase and includes details like total cost, status, and timestamps.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Order Owner',
        help_text='The user who placed the order.',
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Order Status',
        help_text='The current status of the order.'
    )

    total_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0.00,
        verbose_name='Total Price',
        help_text='The total price for the order.',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def calculate_total(self):
        """Calculates and updates the total price for the order."""
        self.total_price = sum(
            item.total_price for item in self.order_items.all()
        )
        self.save()
        return self.total_price

    def cancel(self):
        """
        Cancels the order without modifying stock
         since stock is not deducted for pending orders.
        """
        self.status = 'canceled'
        self.is_active = False

    def complete_order(self):
        """
        Completes the order by deducting stock and updating the status and is_active fields.
        Planned future additions: Locking products to prevent concurrent modifications
        """
        with transaction.atomic():
            for item in self.order_items.all():
                product = item.product

                available_stock = product.get_available_stock()
                effective_available_stock = available_stock + item.quantity

                if item.quantity > effective_available_stock:
                    raise ValidationError(
                        f"Not enough stock for {product}. Available: {available_stock}."
                    )

                product.stock -= item.quantity
                product.save()

            self.status = 'completed'
            self.is_active = False


class OrderItem(models.Model):
    """
    Represents each individual product in the order.
    It keeps track of the quantity and price for each item.
    """

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        verbose_name='Content Type',
        help_text="The type of the product (e.g., plant, gift).",
    )

    object_id = models.PositiveIntegerField(
        help_text="The ID of the product being referenced.",
    )

    product = GenericForeignKey(
        'content_type',
        'object_id')

    order = models.ForeignKey(
        to='orders.Order',
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Order',
        help_text='The order this item belongs to.'
    )

    quantity = models.PositiveIntegerField(
        help_text='Provide order quantity.',
        verbose_name='Product Quantity',
        validators=(
            MaxQuantityValidator(max_quantity=30),
        )
    )

    current_stock = models.PositiveIntegerField(
        help_text="Product stock at the time of order.",
        editable=False,
    )

    price_per_unit = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Price',
        help_text='Price per unit at the time of order.',
    )

    # max_digits for total_price=max_digits for price_per_unit+[log10(max_quantity)]
    total_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name='Total Price',
        help_text='The total price for this item.',
    )

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        """Calculates total price during save."""
        if not self.pk:
            available_stock = self.product.get_available_stock()
            if self.quantity > available_stock:
                raise ValidationError(
                    {'quantity': f"Requested quantity exceeds available stock ({available_stock} available)."}
                )
            self.price_per_unit = self.product.price
            self.current_stock = self.product.stock

        self.total_price = self.quantity * self.price_per_unit

        self.full_clean()

        super().save(*args, **kwargs)
