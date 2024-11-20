from django.shortcuts import render
from django.views.generic import ListView


def show_flowers_list(request):
    return render(request, 'flowers/flowers-list.html')

class FlowersListView(ListView):
    template_name = 'flowers/flowers-list.html'


