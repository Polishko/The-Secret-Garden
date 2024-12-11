from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from thesecretgarden.common.serializers import ContactMessageSerializer
from thesecretgarden.flowers.models import Plant
from thesecretgarden.gifts.models import Gift


def landing_page(request):
    """Displays the landing page"""
    return render(request, 'common/landing-page.html', {'is_landing_page': True})


class BaseBulkCreateView(FormView):
    """
    A base view for bulk creating instances of a model using a formset.

    Features:
    - Renders a formset with multiple forms for creating instances.
    - Handles validation and displays errors per form.
    - Supports marking forms for deletion via a `DELETE` field.
    - Redirects to a success URL upon successful creation of all valid forms.
    - Provides extensibility for specific models and form classes.
    """
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
    """Displays the contact page"""
    template_name = 'common/contact-us.html'


class AboutUs(TemplateView):
    """Displays the about page"""
    template_name = 'common/about-us.html'

# Note: Added authentication permission requirement to the ContactMessageApiView
# at last moment because of the following project requirement:
# Unauthenticated users (public part) have only 'get' permissions, e.g., landing page, details,
# about page, and login/ register 'post' permissions.
# Future improvement: Add relation to the logged user who sends the message and only allow for customers.
class ContactMessageApiView(APIView):
    """
    API view for handling contact message submissions.

    - Accepts POST requests with contact message data.
    - Validates the data using `ContactMessageSerializer`.
    - Saves the message if valid and returns a success response with HTTP 201.
    - Returns validation errors with HTTP 400 if the data is invalid.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Message sent successfully!'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def custom_404_view(request, exception=None):
    """
    Used to simulate the custom 404 during development
    """
    return render(request, '404.html', status=404)

def get_products(product_type):
    """
    Used in related_products view to retrieve related products based on model
    """
    if product_type == 'plant':
        return Plant.objects.filter(~Q(stock=0)).order_by('-created_at')[:5]
    elif product_type == 'gift':
        return Gift.objects.filter(~Q(stock=0)).order_by('-created_at')[:5]
    else:
        return []

async def related_products(request, product_type):
    """
    Asynchronously fetches and returns related products based on the given product type.
    - Fetches products using the `get_products` function asynchronously.
    - Iterates over the query results and constructs a list of product details,
    including slug, name, price, and image URL.
    - Returns the product data as a JSON response.
    """
    query = await sync_to_async(get_products)(product_type)

    products = []
    async for product in query:
        products.append({
            'slug': product.slug,
            'name': product.name if product_type == 'plant' else f'{product.short_name}',
            'price': product.price,
            'image': product.photo.url,
        })

    return JsonResponse({'products': products})
