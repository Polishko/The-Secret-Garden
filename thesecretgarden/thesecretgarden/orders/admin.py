from django.contrib import admin, messages

from thesecretgarden.orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('user', 'total_price', 'created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'status', 'total_price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            readonly_fields += ('user', 'total_price')
        return readonly_fields

    def save_model(self, request, obj, form, change):
        if not obj.user:
            messages.error(request, "The 'user' field is required for creating an order.")
            return

        if change:
            messages.info(request, f"Order #{obj.id} has been updated by {request.user.username}.")
        super().save_model(request, obj, form, change)
