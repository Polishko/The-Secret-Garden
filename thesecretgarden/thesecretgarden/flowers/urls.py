from django.urls import path

from thesecretgarden.flowers.views import PlantsListView, PlantBulkCreateView

urlpatterns = [
    path('', PlantsListView.as_view(), name='plants-list'),
    path('bulk-create/', PlantBulkCreateView.as_view(), name='plant-bulk-create'),
]
