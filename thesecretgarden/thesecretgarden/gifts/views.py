from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView

from thesecretgarden.common.views import BaseBulkCreateView
from thesecretgarden.gifts.forms import GiftBulkCreateForm
from thesecretgarden.gifts.models import Gift


class GiftsListView(ListView):
    model = Gift
    template_name = 'gifts/gifts-list.html'
    context_object_name = 'items'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity_name'] = 'Gifts'
        return context


class GiftBulkCreateView(BaseBulkCreateView, UserPassesTestMixin):
    template_name = 'gifts/gift-bulk-create.html'
    form_class = GiftBulkCreateForm
    model = Gift

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy('gifts-list')
