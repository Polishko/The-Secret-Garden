from django.contrib import admin


class StockManagementAdminMixin:
    @admin.action(description='Mark as out of stock')
    def mark_as_out_of_stock(model, request, queryset):
        queryset.update(stock=0)