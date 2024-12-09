from django.urls import path, include

from thesecretgarden.orders.views import AddToCardView, CartView, RemoveCartItemView, OrderConfirmView, \
    CompletedOrdersView, OrderCheckOutView, CompletedOrderDetailView, OrderCancelView

urlpatterns = [
    path('<slug:user_slug>/<str:product_type>/<int:product_id>/add-to-cart/', AddToCardView.as_view(), name='add-to-cart'),
    path('<slug:user_slug>/cart/', include([
        path('', CartView.as_view(), name='shopping-cart'),
        path('item/remove/<int:item_id>/', RemoveCartItemView.as_view(), name='remove-item'),
        path('check-out/', OrderCheckOutView.as_view(), name='order-checkout'),
        path('order-confirm/', OrderConfirmView.as_view(), name='order-confirm'),
        path('order-cancel/', OrderCancelView.as_view(), name='order-cancel'),
    ])),
    path('<slug:user_slug>/completed-orders/', include([
        path('', CompletedOrdersView.as_view(), name='completed-orders'),
        path('<int:pk>/', CompletedOrderDetailView.as_view(), name='completed-order-detail'),
    ])),
]
