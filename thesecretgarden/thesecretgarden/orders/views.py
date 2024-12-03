from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views.generic import View

from thesecretgarden.flowers.models import Plant
from thesecretgarden.gifts.models import Gift
from thesecretgarden.mixins import CustomPermissionMixin
from thesecretgarden.orders.models import Order, OrderItem


class AddToCardView(LoginRequiredMixin, CustomPermissionMixin, View):
    def test_func(self):
        """
        Ensures the user is in the 'Customer' group.
        """
        return self.request.user.groups.filter(name='Customer').exists()

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

        order_item.quantity += quantity

        try:
            order_item.save()
        except ValidationError as e:
            return redirect(request.META.get('HTTP_REFERER', 'plants-list'))

        return redirect(request.META.get('HTTP_REFERER', 'plants-list'))


class CartView(LoginRequiredMixin, CustomPermissionMixin, View):
    template_name = 'orders/shopping_cart.html'

    def test_func(self):
        """
        Ensures the user is in the 'Customer' group.
        """
        return self.request.user.groups.filter(name='Customer').exists()

    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user, status='pending').first()
        order_items = []

        if order:
            try:
                order.save()

                for item in order.order_items.all():
                    product = item.product
                    product_type = 'plant' if isinstance(product, Plant) else 'gift'
                    product_name = 'name' if isinstance(product, Plant) else 'brand_name'
                    product_page = 'plant-detail' if isinstance(product, Plant) else 'gift-detail'

                    order_items.append({
                        'id': item.id,
                        'product': product,
                        'quantity': item.quantity,
                        'product_type': product_type,
                        'product_id': product.id,
                        'product_name': product_name,
                        'product_page': product_page,
                        'product_slug': product.slug,
                    })

                context = {
                    'order': order,
                    'order_items': order_items,
                    'total_cost': sum(item['product'].price * item['quantity'] for item in order_items),
                }

                return render(request, self.template_name, context)

            except AttributeError as e:
                messages.error(request, "An error occurred while loading your cart.")
                return redirect('plants-list')

        else:
            messages.info(request, "You have no active orders.")
            context = {
                'order': None,
                'order_items': [],
                'total_cost': 0,
            }
            return render(request, self.template_name, context)


class RemoveCartItemView(LoginRequiredMixin, CustomPermissionMixin, View):
    def test_func(self):
        """
        Ensures the user is in the 'Customer' group.
        """
        return self.request.user.groups.filter(name='Customer').exists()
    
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        order_item = OrderItem.objects.filter(id=item_id, order__user=request.user, order__status='pending').first()

        if order_item:
            try:
                order_item.delete()
                order_item.order.save()
            except Exception as e:
                messages.error(request, "An error occurred while updating your cart.")
        else:
            messages.error(request, "Item not found or unauthorized access.")

        return redirect('shopping-cart')
