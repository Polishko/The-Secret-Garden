from django.contrib import admin

from thesecretgarden.gifts.models import Gift
from thesecretgarden.mixins import StockManagementAdminMixin


@admin.register(Gift)
class GiftAdmin(StockManagementAdminMixin, admin.ModelAdmin):

    list_display = ('brand_name', 'short_name', 'short_description',
                    'type', 'price', 'stock', 'available_stock', 'reserved_stock', 'slug')
    list_filter = ('type', 'price', 'stock')
    search_fields = ('brand_name', 'short_name')
    ordering = ('brand_name',)
    readonly_fields = ('slug', 'available_stock', 'reserved_stock',)

    fieldsets = (
        (None, {'fields': ('brand_name', 'type', 'slug')}),
        ('Details', {'fields': ('short_name', 'short_description', 'price', 'stock', 'photo')}),
    )

    actions = ['mark_as_out_of_stock',]
