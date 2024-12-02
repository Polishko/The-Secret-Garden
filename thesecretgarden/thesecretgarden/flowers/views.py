from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.context_processors import messages
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from thesecretgarden.common.views import BaseBulkCreateView
from thesecretgarden.flowers.forms import PlantBulkCreateForm, PlantCreateForm, PlantEditForm, PlantDeleteForm
from thesecretgarden.flowers.models import Plant


class PlantsListView(ListView):
    model = Plant
    template_name = 'flowers/plants-list.html'
    context_object_name = 'items'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = 'Flowers'
        context['detail_url_name'] = 'plant-detail'
        return context


class PlantBulkCreateView(BaseBulkCreateView, UserPassesTestMixin):
    template_name = 'flowers/plant-bulk-create.html'
    form_class = PlantBulkCreateForm
    model = Plant

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Customizes the behavior for unauthorized access.
        """
        messages.error(self.request, 'You do not have permission to perform this action.')
        return redirect('plants-list')

    def get_success_url(self):
        return reverse_lazy('plants-list')


class PlantCreateView(CreateView, UserPassesTestMixin):
    model = Plant
    form_class = PlantCreateForm
    template_name = 'flowers/plant-create-edit.html'
    success_url = reverse_lazy('plants-list')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Customizes the behavior for unauthorized access.
        """
        messages.error(self.request, 'You do not have permission to perform this action.')
        return redirect('plants-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = 'Plant'
        context['cancel_return_view'] = reverse_lazy('plants-list')
        return context


class PlantDetailView(DetailView):
    model = Plant
    template_name = 'flowers/plant-detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class PlantEditView(UpdateView, UserPassesTestMixin):
    model = Plant
    form_class = PlantEditForm
    template_name = 'flowers/plant-create-edit.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Customizes the behavior for unauthorized access.
        """
        messages.error(self.request, 'You do not have permission to perform this action.')
        return redirect('plants-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        context['item'] = 'Plant'
        context['cancel_return_view'] =  reverse_lazy('plant-detail', kwargs={'slug': self.object.slug})
        return context

    def get_success_url(self):
        return reverse_lazy('plant-detail', kwargs={'slug': self.object.slug})


class PLantDeleteView(DeleteView, UserPassesTestMixin):
    model = Plant
    template_name = 'flowers/plant-delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('plants-list')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Customizes the behavior for unauthorized access.
        """
        messages.error(self.request, 'You do not have permission to perform this action.')
        return redirect('plants-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PlantDeleteForm(instance=self.object)
        context['is_delete'] = True
        context['product'] = 'Plant'
        context['cancel_return_view'] = reverse_lazy('plant-detail', kwargs={'slug': self.object.slug})
        return context

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except IntegrityError:
            messages.error(request, 'This plant cannot be deleted as it is associated with an order.')
            return redirect(reverse_lazy('plant-detail', kwargs={'slug': self.object.slug}))
