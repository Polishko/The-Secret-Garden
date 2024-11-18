from django.contrib import admin

from thesecretgarden.flowers.models import Plant
from thesecretgarden.mixins import StockManagementAdminMixin


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin, StockManagementAdminMixin):

    list_display = ('name', 'type', 'price', 'stock', 'slug')
    list_filter = ('type', 'price', 'stock')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('slug',)

    fieldsets = (
        (None, {'fields': ('name', 'type', 'slug')}),
        ('Details', {'fields': ('description', 'price', 'stock', 'photo')}),
    )

    actions = ['mark_as_out_of_stock']
