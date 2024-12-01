from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View

from thesecretgarden.flowers.models import Plant
from thesecretgarden.gifts.models import Gift
from thesecretgarden.orders.models import Order, OrderItem


class AddToCardView(View):
    def post(self, request, *args, **kwargs):
        """
        Handles adding items to the cart (pending orders).
        """
        product_type = kwargs.get('product_type')
        product_id = kwargs.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        model = Plant if product_type == 'plant' else Gift
        product = model.objects.get(pk=product_id)

        order, _ = Order.objects.get_or_create(user=request.user, status='pending')

        content_type = ContentType.objects.get_for_model(model)
        order_item, item_created = OrderItem.objects.get_or_create(
            order=order,
            content_type=content_type,
            object_id=product.pk,
            defaults={'quantity': 0, 'price_per_unit': product.price}
        )

        # Update the quantity
        order_item.quantity += quantity

        try:
            order_item.save()  # Let the model's clean handle validation
        except ValidationError as e:
            messages.error(request, e.message_dict.get('quantity', 'An error occurred.'))
            return redirect(request.META.get('HTTP_REFERER', 'plants-list'))

        messages.success(request, f"Added {quantity} units to your cart.")
        return redirect(request.META.get('HTTP_REFERER', 'plants-list'))