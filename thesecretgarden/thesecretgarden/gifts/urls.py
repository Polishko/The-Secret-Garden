from django.urls import path


from thesecretgarden.gifts.views import GiftsListView, GiftBulkCreateView
urlpatterns = [
    path('', GiftsListView.as_view(), name='gifts-list'),
    path('bulk-create/', GiftBulkCreateView.as_view(), name='gift-bulk-create'),
]
