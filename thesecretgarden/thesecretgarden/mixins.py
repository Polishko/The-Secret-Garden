from django.contrib import admin, messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class PlaceHolderMixin:
    def add_placeholder(self):
        if hasattr(self, 'fields') and hasattr(self, 'initial'):
            for field_name, field in self.fields.items():
                value = self.initial.get(field_name, '')
                if not value:
                    field.widget.attrs.setdefault('placeholder', f"Enter your {field_name.replace('_', ' ')}")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholder()


class HideHelpTextMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'fields'):
            for field in self.fields.values():
                field.help_text = None


class DisableFieldMixin:
    def make_fields_readonly(self):
        readonly_fields = getattr(self, 'readonly_fields', [])

        if hasattr(self, 'fields'):
            for field_name in self.fields.keys():
                if field_name in readonly_fields:
                    self.fields[field_name].widget.attrs['disabled'] = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.make_fields_readonly()


class StockManagementAdminMixin:
    @admin.action(description='Mark as out of stock')
    def mark_as_out_of_stock(self, request, queryset):
        """
        Marks selected items as out of stock, only if none are reserved.
        """
        for item in queryset:
            if item.stock != item.get_available_stock():
                self.message_user(
                    request,
                    f'Cannot mark items as out of stock, there are reserved items.',
                    messages.ERROR
                )
                return

        queryset.update(stock=0)
        self.message_user(
            request,
            f'{queryset.count()} items successfully marked as out of stock.',
            messages.SUCCESS
        )

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of reserved items.
        """
        if obj:
            if obj.stock != obj.get_available_stock():
                item_name = getattr(obj, 'brand_name', getattr(obj, 'name', 'this item'))
                self.message_user(
                    request,
                    f'Reminder: {item_name} cannot be deleted as it is reserved. Remove order item first',
                    messages.ERROR
                )
                return False
        return super().has_delete_permission(request, obj)

    def available_stock(self, obj):
        return obj.get_available_stock()
    available_stock.short_description = 'Available Stock'

    def reserved_stock(self, obj):
        return obj.stock - obj.get_available_stock()
    reserved_stock.short_description = 'Reserved Stock'


class CustomPermissionMixin(UserPassesTestMixin):
    permission_denied_message = 'You do not have permission to access this page.'
    redirect_url = 'plant-list'

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.redirect_url)

    def test_func(self):
        raise NotImplementedError('You must define the `test_func` method.')
