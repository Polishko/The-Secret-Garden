from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from thesecretgarden.accounts.forms import AppUserChangeForm, AppUserCreateForm

UserModel = get_user_model()

@admin.register(UserModel)
class AppUserAdmin(UserAdmin):
    ROLE_PERMISSIONS = {
        'customer': {'is_staff': False, 'is_superuser': False},
        'staff': {'is_staff': True, 'is_superuser': False},
        'admin': {'is_staff': True, 'is_superuser': True},
    }

    add_form = AppUserCreateForm
    form = AppUserChangeForm

    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'last_login',) # visualized fields
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    # visualization categories
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # what fields to show when creating a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Users other than superusers cannot edit email, username, role.
        """
        if not request.user.is_superuser:
            return ['role', 'username', 'email']
        return []

    def update_permissions_based_on_role(self, obj):
        """
        Update is_staff and is_superuser based on role using the ROLE_PERMISSIONS dict.
        """
        role_permissions = self.ROLE_PERMISSIONS.get(obj.role, {'is_staff': False, 'is_superuser': False})
        obj.is_staff = role_permissions['is_staff']
        obj.is_superuser = role_permissions['is_superuser']

    def save_model(self, request, obj, form, change):
        """
        Automatically update is_staff and is_superuser based on role.
        """
        self.update_permissions_based_on_role(obj)
        super().save_model(request, obj, form, change)
