from django.contrib import admin, messages
from django.db import IntegrityError
from django.shortcuts import redirect

from thesecretgarden.flowers.models import Plant
from thesecretgarden.mixins import StockManagementAdminMixin


@admin.register(Plant)
class PlantAdmin(StockManagementAdminMixin, admin.ModelAdmin):

    list_display = ('name', 'type', 'price', 'stock', 'available_stock', 'reserved_stock', 'slug')
    list_filter = ('type', 'price', 'stock')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('slug', 'available_stock', 'reserved_stock',)

    fieldsets = (
        (None, {'fields': ('name', 'type', 'slug')}),
        ('Details', {'fields': ('description', 'price', 'stock', 'photo')}),
    )

    actions = ['mark_as_out_of_stock',]
