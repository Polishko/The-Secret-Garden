from django.contrib import admin
from django.contrib.admin import StackedInline
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from thesecretgarden.accounts.forms import AppUserChangeForm, AppUserForm
from thesecretgarden.accounts.models import Profile

UserModel = get_user_model()

class ProfileInline(StackedInline):
    model = Profile
    can_delete = False
    fields = ('first_name', 'last_name', 'preferred_flower_type',)

@admin.register(UserModel)
class AppUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    add_form = AppUserForm
    form = AppUserChangeForm

    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'last_login',)
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'uuid')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['role', 'username', 'email']
        return ['uuid']
