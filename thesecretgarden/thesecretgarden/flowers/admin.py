from django.contrib import admin

from thesecretgarden.flowers.models import Plant


@admin.action(description='Mark as out of stock')
def mark_as_out_of_stock(model, request, queryset):
    queryset.update(stock=0)


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):

    list_display = ('name', 'type', 'price', 'stock', 'slug')
    list_filter = ('type', 'price', 'stock')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('slug',)

    fieldsets = (
        (None, {'fields': ('name', 'type', 'slug')}),
        ('Details', {'fields': ('description', 'price', 'stock', 'photo')}),
    )

    actions = [mark_as_out_of_stock]
