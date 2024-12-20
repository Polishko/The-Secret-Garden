from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView

from thesecretgarden.flowers.models import Plant
from thesecretgarden.gifts.models import Gift
from thesecretgarden.mixins import IsUserCustomerMixin
from thesecretgarden.orders.models import Order, OrderItem

from django.db import transaction
from django.shortcuts import redirect

class AddToCardView(LoginRequiredMixin, IsUserCustomerMixin, View):
    def post(self, request, *args, **kwargs):
        """Handles adding items to the cart (pending orders)."""
        user_slug = kwargs.get('user_slug')
        if user_slug != request.user.slug:
            return redirect('plants-list')

        product_type = kwargs.get('product_type')
        product_id = kwargs.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        model = Plant if product_type == 'plant' else Gift
        product = model.objects.get(pk=product_id)

        available_stock = product.get_available_stock()
        if quantity > available_stock:
            return redirect(request.META.get('HTTP_REFERER', 'plants-list'))

        with transaction.atomic():
            order, created = Order.objects.get_or_create(user=request.user, status='pending')

            content_type = ContentType.objects.get_for_model(model)
            order_item, item_created = OrderItem.objects.get_or_create(
                order=order,
                content_type=content_type,
                object_id=product.pk,
                defaults={'quantity': 0, 'price_per_unit': product.price}
            )

            order_item.quantity += quantity
            order_item.save()

        return redirect(request.META.get('HTTP_REFERER', 'plants-list'))


class CartView(LoginRequiredMixin, IsUserCustomerMixin, View):
    """Displays current cart items"""
    template_name = 'orders/shopping-cart.html'

    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user, status='pending').first()
        order_items = []

        user_slug = kwargs.get('user_slug')
        if user_slug != request.user.slug:
            return redirect('plants-list')

        if order:
            try:
                order.save()

                for item in order.order_items.all():
                    product = item.product
                    product_type = 'plant' if isinstance(product, Plant) else 'gift'
                    product_name = 'name' if isinstance(product, Plant) else 'brand_name'
                    product_page = 'plant-detail' if isinstance(product, Plant) else 'gift-detail'

                    dynamic_stock = product.get_available_stock() + item.quantity

                    order_items.append({
                        'id': item.id,
                        'product': product,
                        'quantity': item.quantity,
                        'product_type': product_type,
                        'product_id': product.id,
                        'product_name': product_name,
                        'product_page': product_page,
                        'product_slug': product.slug,
                        'dynamic_stock': dynamic_stock,
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
            context = {
                'order': None,
                'order_items': [],
                'total_cost': 0,
            }
            return render(request, self.template_name, context)


class RemoveCartItemView(LoginRequiredMixin, IsUserCustomerMixin, View):
    """Removes items from shopping cart"""
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        order_item = OrderItem.objects.filter(id=item_id, order__user=request.user, order__status='pending').first()

        user_slug = kwargs.get('user_slug')
        if user_slug != request.user.slug:
            return redirect('plants-list')

        if order_item:
            try:
                order_item.delete()
                order_item.order.save()
            except Exception as e:
                messages.error(request, "An error occurred while updating your cart.")
        else:
            messages.error(request, "Item not found or unauthorized access.")

        return redirect('shopping-cart', user_slug)


class OrderCheckOutView(LoginRequiredMixin, IsUserCustomerMixin, View):
    """Displays order checkout page"""
    template_name = 'orders/order-checkout.html'

    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user, status='pending').first()

        user_slug = kwargs.get('user_slug')
        if user_slug != request.user.slug:
            return redirect('plants-list')

        if not order:
            messages.error(request, "Order not found or unauthorized access.")
            return redirect('shopping-cart', user_slug)

        try:
            if order.total_price == 0 or order.total_price != order.calculate_total():
                order.calculate_total()
            context = {'order_sum': order.total_price}
        except Exception as e:
            messages.error(request, f"An error occurred while calculating your order: {str(e)}")
            return redirect('shopping-cart', user_slug)

        return render(request, self.template_name, context)


class OrderConfirmView(LoginRequiredMixin, IsUserCustomerMixin, View):
    """Confirms the order"""
    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user, status='pending').first()

        user_slug = kwargs.get('user_slug')
        if user_slug != request.user.slug:
            return redirect('plants-list')

        if not order:
            messages.error(request, "Order not found or unauthorized access.")
            return redirect('shopping-cart', user_slug)

        profile = request.user.profile
        if not profile.address:
            messages.error(
                request,
                'You must provide an address to place an order.'
            )

            return redirect('profile-edit', user_slug)

        try:
            order.complete_order()
            order.save()
            messages.success(request, "Your order has been successfully completed!")
            return redirect('completed-order-detail', user_slug=user_slug, pk=order.pk)
        except ValidationError as e:
            error_message = ', '.join(e.messages)
            messages.error(request, f"Order could not be completed: {error_message}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

        return redirect('shopping-cart', user_slug)


class OrderCancelView(LoginRequiredMixin, IsUserCustomerMixin, View):
    """Cancel the order"""
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, user=request.user, status='pending')

        user_slug = kwargs.get('user_slug')
        if user_slug != request.user.slug:
            return redirect('plants-list')

        try:
            order.cancel()
            order.save()
            messages.success(request, "Your order has been canceled!")
        except ValidationError as e:
            error_message = ', '.join(e.messages)  # Extract messages from ValidationError
            messages.error(request, f"Order could not be canceled: {error_message}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

        return redirect('plants-list')


class CompletedOrdersView(LoginRequiredMixin, IsUserCustomerMixin, ListView):
    """Displays completed orders page"""
    model = Order
    template_name = 'orders/orders-list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status='completed', is_active=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Your Completed Orders'
        context['empty_message'] = 'completed orders'
        return context


class CompletedOrderDetailView(LoginRequiredMixin, IsUserCustomerMixin, DetailView):
    """Displays completed order details"""
    model = Order
    template_name = 'orders/completed-order-detail.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        order_id = self.kwargs.get('pk')
        return get_object_or_404(Order, pk=order_id, user=self.request.user, status='completed', is_active=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()

        order_items = []
        for item in order.order_items.all():
            product_type = 'plant' if item.content_type == ContentType.objects.get_for_model(Plant) else 'gift'
            product_name = item.product.name if item.content_type == ContentType.objects.get_for_model(Plant) \
                else f'{item.product.brand_name} {item.product.short_name}'
            order_items.append({
                'product': item.product,
                'quantity': item.quantity,
                'price_per_unit': item.price_per_unit,
                'total_price': item.total_price,
                'product_type': product_type,
                'product_name': product_name
            })

        context['order_items'] = order_items
        return context

# Future improvement: Consider and test moving address validation to dispatch for better flow and early validation.
