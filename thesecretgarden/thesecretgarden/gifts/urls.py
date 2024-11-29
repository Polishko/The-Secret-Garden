from django.urls import path, include

from thesecretgarden.gifts.views import GiftsListView, GiftBulkCreateView, GiftCreateView, GiftDetailView, GiftEditView, \
    GiftDeleteView

urlpatterns = [
    path('', GiftsListView.as_view(), name='gifts-list'),
    path('bulk-create/', GiftBulkCreateView.as_view(), name='gift-bulk-create'),
path('create/', GiftCreateView.as_view(), name='gift-create-edit'),
    path('<slug:slug>/', include([
        path('detail/', GiftDetailView.as_view(), name='gift-detail'),
        path('edit/', GiftEditView.as_view(), name='gift-create-edit'),
        path('delete/', GiftDeleteView.as_view(), name='gift-delete'),
    ])),
]
