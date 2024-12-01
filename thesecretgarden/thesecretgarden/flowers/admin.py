from django.contrib import admin, messages
from django.db import IntegrityError
from django.shortcuts import redirect

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

    def delete_model(self, request, obj):
        try:
            obj.delete()
        except IntegrityError:
            messages.error(request, "This plant cannot be deleted as it is associated with an order.")
            return redirect('admin:flowers_plant_changelist')  # Redirect to the Plant list in admin
