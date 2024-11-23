from django.urls import reverse_lazy
from django.views.generic import ListView

from thesecretgarden.common.views import BaseBulkCreateView
from thesecretgarden.flowers.forms import PlantBulkCreateForm
from thesecretgarden.flowers.models import Plant


class PlantsListView(ListView):
    model = Plant
    template_name = 'flowers/plants-list.html'
    context_object_name = 'plants'


class PlantBulkCreateView(BaseBulkCreateView):
    template_name = 'flowers/plant-bulk-create.html'
    form_class = PlantBulkCreateForm
    model = Plant

    def get_success_url(self):
        return reverse_lazy('plants-list')
