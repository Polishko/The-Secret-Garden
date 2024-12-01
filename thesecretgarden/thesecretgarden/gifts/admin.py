from django.contrib import admin, messages
from django.db import IntegrityError
from django.shortcuts import redirect


from thesecretgarden.gifts.models import Gift
from thesecretgarden.mixins import StockManagementAdminMixin


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin, StockManagementAdminMixin):

    list_display = ('brand_name', 'short_name', 'short_description', 'type', 'price', 'stock', 'slug')
    list_filter = ('type', 'price', 'stock')
    search_fields = ('brand_name', 'short_name')
    ordering = ('brand_name',)
    readonly_fields = ('slug',)

    fieldsets = (
        (None, {'fields': ('brand_name', 'type', 'slug')}),
        ('Details', {'fields': ('short_name', 'short_description', 'price', 'stock', 'photo')}),
    )

    actions = ['mark_as_out_of_stock']

    def delete_model(self, request, obj):
        try:
            obj.delete()
        except IntegrityError:
            messages.error(request, "This gift cannot be deleted as it is associated with an order.")
            return redirect('admin:gifts_gift_changelist')  # Redirect to the Gift list in admin
