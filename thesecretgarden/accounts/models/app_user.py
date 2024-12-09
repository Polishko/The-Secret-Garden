import logging

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

from django.db import models
from django.utils.text import slugify

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

    slug = models.SlugField(
        unique=True,
        editable=False,
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
    REQUIRED_FIELDS = ['email']

    def clean(self):
        super().clean()
        if self.role == 'admin' and not self.is_superuser:
            raise ValidationError("Admin role requires the user to be a superuser.")

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_base = slugify(self.username.lower())
            slug = slug_base
            counter = 1
            while AppUser.objects.filter(slug=slug).exists():
                slug = f"{slug_base}-{counter}"
                counter += 1
            self.slug = slug

        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.username}'
