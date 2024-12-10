from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect
from django.urls import reverse

from thesecretgarden.accounts.forms import AppUserChangeForm, AppUserCreateForm
from thesecretgarden.accounts.models import Profile

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

    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'last_login',)
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

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
        readonly_fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            return readonly_fields + ('role', 'username', 'email')
        return readonly_fields

    def update_permissions_based_on_role(self, obj):
        """
        Update is_staff and is_superuser based on role using the ROLE_PERMISSIONS dict.
        """
        role_permissions = self.ROLE_PERMISSIONS.get(obj.role, {'is_staff': False, 'is_superuser': False})
        obj.is_staff = role_permissions['is_staff']
        obj.is_superuser = role_permissions['is_superuser']

    def delete_queryset(self, request, queryset):
        """
        Prevent bulk deletion of users who are associated with orders.
        """
        restricted_users = queryset.filter(orders__isnull=False)

        if restricted_users.exists():
            usernames = ', '.join(restricted_users.values_list('username', flat=True))
            messages.error(
                request,
                f"Cannot delete the following users because they are associated with orders: {usernames}"
            )
            queryset = queryset.exclude(pk__in=restricted_users.values_list('pk', flat=True))

        super().delete_queryset(request, queryset)

    def message_user(self, request, message, level=messages.SUCCESS, extra_tags='', fail_silently=False):
        """
        Suppress the default success message after a blocked deletion.
        """
        if "Successfully deleted" in message and level == messages.SUCCESS:
            return
        super().message_user(request, message, level, extra_tags, fail_silently)

    def save_model(self, request, obj, form, change):
        """
        Automatically update is_staff and is_superuser based on role.
        """
        self.update_permissions_based_on_role(obj)
        super().save_model(request, obj, form, change)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'first_name', 'last_name', 'preferred_flower_type')
    list_filter = ('preferred_flower_type', 'is_active')
    list_display = ('user', 'first_name', 'last_name', 'preferred_flower_type', 'is_active')
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('user', 'first_name', 'last_name', 'preferred_flower_type')}),
        ('Contact Info', {'fields': ('address', 'phone')}),
        ('Status', {'fields': ('is_active', 'created_at', 'updated_at')}),
    )

    def delete_queryset(self, request, queryset):
        """
        Prevent bulk deletion of profiles.
        """
        messages.error(
            request,
            "Profiles cannot be deleted directly. Delete the associated users instead."
        )
        return

    def message_user(self, request, message, level=messages.SUCCESS, extra_tags='', fail_silently=False):
        """
        Suppress the default success message after a blocked deletion.
        """
        if "Successfully deleted" in message and level == messages.SUCCESS:
            return
        super().message_user(request, message, level, extra_tags, fail_silently)

    def add_view(self, request, form_url='', extra_context=None):
        """
        Prevent profile creation directly from the admin panel.
        """
        messages.error(
            request,
            "Profiles cannot be created directly. A profile is automatically created when a user is added."
        )
        return HttpResponseRedirect(reverse('admin:accounts_profile_changelist'))

    def delete_view(self, request, object_id, extra_context=None):
        """
        Override the default delete view to prevent direct Profile deletion
        and guide the admin to delete the related User instead.
        """
        profile = self.get_object(request, object_id)

        if profile:
            messages.error(
                request,
                f"You cannot delete the profile directly."
                f" Instead, delete the associated user: {profile.user.username}."
            )
            # Redirect to the user's admin page
            user_admin_url = reverse('admin:accounts_appuser_change', args=[profile.user.pk])
            return HttpResponseRedirect(user_admin_url)

        return super().delete_view(request, object_id, extra_context)
