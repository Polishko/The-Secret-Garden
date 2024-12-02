from django.contrib import admin, messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class StockManagementAdminMixin:
    @admin.action(description='Mark as out of stock')
    def mark_as_out_of_stock(model, request, queryset):
        queryset.update(stock=0)


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


class CustomPermissionMixin(UserPassesTestMixin):
    permission_denied_message = "You do not have permission to access this page."
    redirect_url = "plant-list"

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.redirect_url)

    def test_func(self):
        raise NotImplementedError("You must define the `test_func` method.")
