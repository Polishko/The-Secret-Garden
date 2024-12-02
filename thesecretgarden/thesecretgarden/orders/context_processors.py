from thesecretgarden.orders.models import Order

def cart_item_count(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, status='pending').first()
        if order:
            return {'cart_item_count': sum(item.quantity for item in order.order_items.all())}
    return {'cart_item_count': 0}
