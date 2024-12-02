from django.urls import path, include

from thesecretgarden.orders.views import AddToCardView, CartView, RemoveCartItemView

urlpatterns = [
    path('<str:product_type>/<int:product_id>/add-to-cart/', AddToCardView.as_view(), name='add-to-cart'),
    path('cart/', include([
        path('', CartView.as_view(), name='shopping-cart'),
        path('item/remove/<int:item_id>/', RemoveCartItemView.as_view(), name='remove-item'),
    ])),
]
