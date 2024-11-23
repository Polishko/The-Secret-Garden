from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from django.shortcuts import redirect
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

        has_error = False
        saved_forms = []
        forms_with_errors = []

        for form in formset:
            if form.is_valid():
                if form.cleaned_data.get('DELETE', False):
                    continue  # Skip delete-marked forms

                # Try to save valid forms
                try:
                    form.save()
                    saved_forms.append(form)
                except ValidationError as e:
                    # Handle model-level validation errors
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
                    # Handle other save-related errors
                    has_error = True
                    forms_with_errors.append(form)
                    form.add_error(None, f"An error occurred while saving: {ve}")
            else:
                # If the form is invalid, add it to the errors list
                has_error = True
                forms_with_errors.append(form)

            # Debug information
            print(f"Saved Forms: {len(saved_forms)}")
            print(f"Forms with Errors: {len(forms_with_errors)}")
            print(f"Has Error: {has_error}")

        if not has_error and saved_forms:
            return redirect(self.success_url)

        updated_forms = []
        for form in formset:
            if form.cleaned_data.get('DELETE', False):
                continue  # Exclude deleted forms
            updated_forms.append(form)

        recreated_formset = self.get_formset(data=None, files=None)
        for i, form in enumerate(updated_forms):
            recreated_formset.forms[i] = form

        return self.render_to_response({'formset': recreated_formset})
