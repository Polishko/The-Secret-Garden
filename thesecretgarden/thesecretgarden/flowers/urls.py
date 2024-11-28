from django.urls import path, include

from thesecretgarden.flowers.views import PlantsListView, PlantBulkCreateView, PlantCreateView, PlantDetailView, \
    PlantEditView, PLantDeleteView

urlpatterns = [
    path('', PlantsListView.as_view(), name='plants-list'),
    path('bulk-create/', PlantBulkCreateView.as_view(), name='plant-bulk-create'),
    path('create/', PlantCreateView.as_view(), name='plant-create-edit'),
    path('<slug:slug>/', include([
        path('detail/', PlantDetailView.as_view(), name='plant-detail'),
        path('edit/', PlantEditView.as_view(), name='plant-create-edit'),
        path('delete/', PLantDeleteView.as_view(), name='plant-delete'),
    ])),
]
