from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from thesecretgarden.common.views import BaseBulkCreateView
from thesecretgarden.gifts.forms import GiftBulkCreateForm, GiftCreateForm, GiftEditForm, GiftDeleteForm
from thesecretgarden.gifts.models import Gift
from thesecretgarden.mixins import IsUserStaffMixin


class GiftsListView(ListView):
    model = Gift
    template_name = 'gifts/gifts-list.html'
    context_object_name = 'items'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = 'Gifts'
        context['detail_url_name'] = 'gift-detail'
        return context


class GiftBulkCreateView(LoginRequiredMixin, IsUserStaffMixin, BaseBulkCreateView):
    template_name = 'gifts/gift-bulk-create.html'
    form_class = GiftBulkCreateForm
    model = Gift

    def get_success_url(self):
        return reverse_lazy('gifts-list')


class GiftCreateView(LoginRequiredMixin, IsUserStaffMixin, CreateView):
    model = Gift
    form_class = GiftCreateForm
    template_name = 'gifts/gift-create-edit.html'
    success_url = reverse_lazy('gifts-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = 'Gift'
        context['cancel_return_view'] = reverse_lazy('gifts-list')
        return context


class GiftDetailView(DetailView):
    model = Gift
    template_name = 'gifts/gift-detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_reserved = self.object.get_available_stock() != self.object.stock
        context['is_reserved'] = is_reserved
        return context


class GiftEditView(LoginRequiredMixin, IsUserStaffMixin, UpdateView):
    model = Gift
    form_class = GiftEditForm
    template_name = 'gifts/gift-create-edit.html'
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
        context['item'] = 'Gift'
        context['cancel_return_view'] = reverse_lazy('gift-detail', kwargs={'slug': self.object.slug})
        return context

    def get_success_url(self):
        return reverse_lazy('gift-detail', kwargs={'slug': self.object.slug})


class GiftDeleteView(LoginRequiredMixin, IsUserStaffMixin, DeleteView):
    model = Gift
    template_name = 'gifts/gift-delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('gifts-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GiftDeleteForm(instance=self.object)
        context['is_delete'] = True
        context['product'] = 'Gift'
        context['cancel_return_view'] = reverse_lazy('gift-detail', kwargs={'slug': self.object.slug})
        return context

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except IntegrityError:
            messages.error(request, 'This gift cannot be deleted as it is associated with an order.')
            return redirect(reverse_lazy('gift-detail', kwargs={'slug': self.object.slug}))
