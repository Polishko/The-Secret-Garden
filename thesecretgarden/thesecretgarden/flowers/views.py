from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.context_processors import messages
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from thesecretgarden.common.forms import SearchForm
from thesecretgarden.common.views import BaseBulkCreateView
from thesecretgarden.flowers.forms import PlantBulkCreateForm, PlantCreateForm, PlantEditForm, PlantDeleteForm
from thesecretgarden.flowers.models import Plant
from thesecretgarden.mixins import IsUserStaffMixin


class PlantsListView(ListView):
    ITEMS_PER_PAGE = 6

    model = Plant
    template_name = 'flowers/plants-list.html'
    context_object_name = 'items'
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = 'Flowers'
        context['detail_url_name'] = 'plant-detail'
        context['form'] = SearchForm(self.request.GET)
        context['items_per_page'] = self.ITEMS_PER_PAGE
        return context


class PlantBulkCreateView(LoginRequiredMixin, IsUserStaffMixin, BaseBulkCreateView):
    template_name = 'flowers/plant-bulk-create.html'
    form_class = PlantBulkCreateForm
    model = Plant

    def get_success_url(self):
        return reverse_lazy('plants-list')


class PlantCreateView(LoginRequiredMixin, IsUserStaffMixin, CreateView):
    model = Plant
    form_class = PlantCreateForm
    template_name = 'flowers/plant-create-edit.html'
    success_url = reverse_lazy('plants-list')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_reserved = self.object.get_available_stock() != self.object.stock
        context['is_reserved'] = is_reserved
        return context


class PlantEditView(LoginRequiredMixin, IsUserStaffMixin, UpdateView):
    model = Plant
    form_class = PlantEditForm
    template_name = 'flowers/plant-create-edit.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            available_stock = self.object.get_available_stock()
            reserved_stock = self.object.stock - available_stock
            context['available_stock'] = available_stock
            context['reserved_stock'] = reserved_stock

        except AttributeError as e:
            context['available_stock'] = 0
            context['reserved_stock'] = 0
            messages.error(self.request, "Unable to calculate stock information.")

        except Exception as e:
            context['available_stock'] = 0
            context['reserved_stock'] = 0
            messages.error(self.request, "An unexpected error occurred while loading stock information.")

        context['is_edit'] = True
        context['item'] = 'Plant'
        context['cancel_return_view'] =  reverse_lazy('plant-detail', kwargs={'slug': self.object.slug})
        return context

    def get_success_url(self):
        return reverse_lazy('plant-detail', kwargs={'slug': self.object.slug})


class PlantDeleteView(LoginRequiredMixin, IsUserStaffMixin, DeleteView):
    model = Plant
    template_name = 'flowers/plant-delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('plants-list')

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
