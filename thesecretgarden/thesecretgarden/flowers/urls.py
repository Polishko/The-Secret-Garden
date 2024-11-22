from django.urls import path

from thesecretgarden.flowers.views import BulkCreatePlantView, PlantsListView

urlpatterns = [
    path('', PlantsListView.as_view(), name='plants-list'),
    path('bulk-create/', BulkCreatePlantView.as_view(), name='plant-bulk-create'),
]
