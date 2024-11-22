from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from thesecretgarden.flowers.forms import PlantBulkCreateForm
from thesecretgarden.flowers.models import Plant


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
            saved_forms = []
            forms_with_errors = []

            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    continue

                if form.cleaned_data:
                    try:
                        form.save()
                        saved_forms.append(form)
                    except ValidationError as e:
                        # Capture model validation errors
                        has_error = True
                        forms_with_errors.append(form)

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
                        forms_with_errors.append(form)
                        form.add_error(None, f"An error occurred while saving: {ve}")
                else:
                    has_error = True # consider empty forms as invalid
                    forms_with_errors.append(form)

            if not has_error:
                return redirect(self.success_url)

            # Ensure successfully saved forms are cleared
            for form in saved_forms:
                form.cleaned_data = {}
                form.data = form.data.copy()
                for field_name, field in form.fields.items():
                    if field.widget.attrs.get('name'):
                        form.data[field.widget.attrs['name']] = ''
                    if isinstance(field, forms.ImageField) and field_name in form.files:
                        form.files.pop(field_name, None)


            recreated_formset = self.get_formset(initial=None)

            for index, form in enumerate(recreated_formset):
                if index < len(forms_with_errors):
                    # Replace new form with the original invalid form
                    recreated_formset.forms[index] = forms_with_errors[index]

            formset = recreated_formset

        return self.render_to_response({'formset': formset})

