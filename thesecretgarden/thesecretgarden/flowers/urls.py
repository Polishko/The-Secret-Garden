from django.urls import path, include

from thesecretgarden.flowers.views import show_flowers_list, BulkCreatePlantView

urlpatterns = [
    # path('', FlowersListView.as_view(), name='flowers-list'),
    path('', show_flowers_list, name='plants-list'),
    path('bulk-create/', BulkCreatePlantView.as_view(), name='plant-bulk-create'),
]
