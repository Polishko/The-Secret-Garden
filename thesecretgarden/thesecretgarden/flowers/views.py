from django.shortcuts import render
from django.views.generic import ListView

from thesecretgarden.flowers.models import Plant


def show_flowers_list(request):
    return render(request, 'flowers/flowers-list.html')

class PlantsListView(ListView):
    model = Plant
    template_name = 'flowers/flowers-list.html'
    context_object_name = 'plants'


