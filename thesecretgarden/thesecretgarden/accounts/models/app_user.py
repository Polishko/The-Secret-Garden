from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator

from django.db import models

from django.utils.translation import gettext_lazy as _

from thesecretgarden.accounts.managers import AppUserManager
from thesecretgarden.accounts.validators import UsernameValidator


class AppUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )

    username = models.CharField(
        max_length=30,
        unique=True,
        null=False,
        blank=False,
        validators=(
            MinLengthValidator(3),
            UsernameValidator(),
        ),
        verbose_name='Username',
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        verbose_name='Email',
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='customer',
        verbose_name = 'Role',
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = AppUserManager()

    USERNAME_FIELD = 'username'

    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email', 'role']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
