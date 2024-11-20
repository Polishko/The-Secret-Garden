from django.core.exceptions import ValidationError
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from thesecretgarden.flowers.forms import PlantBulkCreateForm
from thesecretgarden.flowers.models import Plant


def show_flowers_list(request):
    return render(request, 'flowers/plants-list.html')

class PlantsListView(ListView):
    model = Plant
    template_name = 'flowers/plants-list.html'
    context_object_name = 'plants'


class BulkCreatePlantView(FormView):
    template_name = 'flowers/plant-bulk-create.html'
    success_url = reverse_lazy('plants-list')
    form_class = PlantBulkCreateForm

    def get_formset(self, *args, **kwargs):
        PlantFormSet = formset_factory(self.form_class, extra=5, can_delete=True)
        return PlantFormSet(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(request.POST, request.FILES)

        if formset.is_valid():
            has_error = False
            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    continue

                if form.cleaned_data:
                    try:
                        form.save()
                    except ValidationError as e:
                        # Capture model validation errors
                        has_error = True
                        for field, errors in e.message_dict.items():
                            if field in form.fields:
                                for error in errors:
                                    form.add_error(field, error)
                            else:
                                for error in errors:
                                    form.add_error(None, error)
                    except ValueError as ve:
                        # Capture the ValueError from Django's save logic
                        has_error = True
                        form.add_error(None, f"An error occurred while saving: {ve}")
            if not has_error:
                return redirect(self.success_url)

        return self.render_to_response({'formset': formset})

