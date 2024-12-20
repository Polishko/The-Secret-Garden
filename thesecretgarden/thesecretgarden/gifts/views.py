from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, models
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from thesecretgarden.common.forms import SearchForm
from thesecretgarden.common.views import BaseBulkCreateView
from thesecretgarden.gifts.forms import GiftBulkCreateForm, GiftCreateForm, GiftEditForm, GiftDeleteForm
from thesecretgarden.gifts.models import Gift
from thesecretgarden.mixins import IsUserStaffMixin


class GiftsListView(ListView):
    ITEMS_PER_PAGE = 6

    model = Gift
    template_name = 'gifts/gifts-list.html'
    context_object_name = 'items'
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(
                models.Q(brand_name__icontains=query) |
                models.Q(short_name__icontains=query) |
                models.Q(short_description__icontains=query) |
                models.Q(type__icontains=query)
            )
        return queryset.order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = 'Gifts'
        context['detail_url_name'] = 'gift-detail'
        context['form'] = SearchForm(self.request.GET)
        context['items_per_page'] = self.ITEMS_PER_PAGE
        context['is_list_page'] = True
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
        context['product_type'] = 'gift'
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
            messages.error(request, "This gift cannot be deleted as it is associated with an order.")
            return redirect(reverse_lazy('gift-detail', kwargs={'slug': self.object.slug}))

# Future improvement: Consider abstracting shared logic across views to reduce duplication.
# Add non-form-related validations and more detailed error handling messages where applicable.
