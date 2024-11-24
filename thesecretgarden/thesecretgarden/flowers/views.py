from django.urls import reverse_lazy
from django.views.generic import ListView

from thesecretgarden.common.views import BaseBulkCreateView
from thesecretgarden.flowers.forms import PlantBulkCreateForm
from thesecretgarden.flowers.models import Plant


class PlantsListView(ListView):
    model = Plant
    template_name = 'flowers/plants-list.html'
    context_object_name = 'items'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity_name'] = 'Flowers'
        return context


class PlantBulkCreateView(BaseBulkCreateView):
    template_name = 'flowers/plant-bulk-create.html'
    form_class = PlantBulkCreateForm
    model = Plant

    def get_success_url(self):
        return reverse_lazy('plants-list')
