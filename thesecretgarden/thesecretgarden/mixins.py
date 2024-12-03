from django.contrib import admin, messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404

from thesecretgarden.accounts.models import Profile

# Form management mixins
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

# Admin management mixins
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

# Permission mixins
class BasePermissionMixin(UserPassesTestMixin):
    """
    Base mixin for handling permission denied cases with a standard message and redirect.
    """
    permission_denied_message = 'You do not have permission to perform this action.'
    redirect_url = 'plants-list'  # Default redirection

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.redirect_url)

class IsUserProfileOwnerMixin(BasePermissionMixin):
    """
    Ensures the user is the owner of the content. Returns current user.
    """
    permission_denied_message = 'Only content owners can perform this action.'

    def test_func(self):
        return self.request.user.slug == self.kwargs['slug']

    def get_object(self, queryset=None):
        profile = get_object_or_404(Profile, user__slug=self.kwargs['slug'], is_active=True)
        return profile

class IsUserStaffMixin(BasePermissionMixin):
    """
    Ensures the user is staff or superuser.
    """
    permission_denied_message = 'Only staff members can access this page.'

    def test_func(self):
        return (self.request.user.groups.filter(name='Staff').exists()
                or self.request.user.is_staff or self.request.user.is_superuser)


class IsUserCustomerMixin(BasePermissionMixin):
    """
    Ensures the user is in the 'Customer' group.
    """
    permission_denied_message = 'Only customers can access this page.'

    def test_func(self):
        return self.request.user.groups.filter(name='Customer').exists()
