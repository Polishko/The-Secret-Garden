from django.urls import path

from thesecretgarden.orders.views import AddToCardView

urlpatterns = [
    path('<str:product_type>/<int:product_id>/add-to-cart/', AddToCardView.as_view(), name='add-to-cart'),
]
