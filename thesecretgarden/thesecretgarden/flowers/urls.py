from django.urls import path, include

from thesecretgarden.flowers.views import show_flowers_list

urlpatterns = [
    # path('', FlowersListView.as_view(), name='flowers-list'),
    path('', show_flowers_list, name='flowers-list'),
]