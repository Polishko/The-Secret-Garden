from django.core.exceptions import ValidationError
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView


def landing_page(request):
    return render(request, 'common/landing-page.html', {'is_landing_page': True})

class BaseBulkCreateView(FormView):
    template_name = ''
    form_class = None
    model = None

    def get_success_url(self):
        return reverse_lazy('plant-list')

    def get_formset(self, *args, **kwargs):
        ProductFormSet = formset_factory(self.form_class, extra=5, can_delete=True)
        return ProductFormSet(*args, **kwargs)

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
                    continue

                try:
                    form.save()
                    saved_forms.append(form)
                except ValidationError as e:
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
                    has_error = True
                    forms_with_errors.append(form)
                    form.add_error(None, f"An error occurred while saving: {ve}")
            else:
                has_error = True
                forms_with_errors.append(form)
        if has_error:
            real_errors_exist = any(
                not form.cleaned_data.get('DELETE', False) for form in forms_with_errors
            )

            if not real_errors_exist and (
                    saved_forms or all(form.cleaned_data.get('DELETE', False) for form in formset)):

                return redirect(self.get_success_url())

        if not has_error and len(saved_forms) == len(formset):
            return redirect(self.get_success_url())

        updated_forms = []
        for form in formset:
            if form.cleaned_data.get('DELETE', False) or form in saved_forms:
                continue  # Exclude deleted forms
            updated_forms.append(form)

        recreated_formset = self.get_formset(data=None, files=None)
        for i, form in enumerate(updated_forms):
            recreated_formset.forms[i] = form

        return self.render_to_response({'formset': recreated_formset})


class ContactUsView(TemplateView):
    template_name = 'common/contact-us.html'

class AboutUs(TemplateView):
    template_name = 'common/about-us.html'
