from django.core.exceptions import ValidationError
from django.utils import timezone

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.html import strip_tags

from thesecretgarden.accounts.validators import NameValidator, PhoneNumberValidator, BirthdayValidator, AddressValidator

UserModel = get_user_model()


class Profile(models.Model):
    FLOWER_CHOICES = (
        ('non-floral', 'Non Floral Plants'),
        ('floral', 'Floral Plants'),
        ('cactus', 'Cactuses'),
    )

    MIN_BIRTH_YEAR = 1900

    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        validators=(
            NameValidator(field_name='first name'),
        ),
        verbose_name='First Name',
    )

    last_name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        validators=(
            NameValidator(field_name='last name'),
        ),
        verbose_name='Last Name',
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    preferred_flower_type = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=FLOWER_CHOICES,
        verbose_name='Preferred Flower Type',
    )

    address = models.TextField(
        blank=True,
        null=True,
        verbose_name='Address',
        validators=(
            AddressValidator(),
        ),
        help_text='Enter delivery address for home deliveries.'
    )

    phone = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=(
            PhoneNumberValidator(),
        ),
        verbose_name='Phone Number',
        help_text='Enter a valid phone number.'
    )

    birthday = models.DateField(
        blank=True,
        null=True,
        validators=(
            BirthdayValidator(min_year=MIN_BIRTH_YEAR),
        ),
        verbose_name='Date of Birth',
        help_text='Optional. Enter your birthdate for promotions.'
    )

    def clean(self):
        super().clean()

        if self.first_name == self.last_name:
            raise ValidationError('First name and last name cannot be the same!')

    def save(self, *args, **kwargs):
        if self.first_name:
            self.first_name = self.first_name.strip().capitalize()
        if self.last_name:
            self.last_name = self.last_name.strip().capitalize()

        if self.address:
            self.address = ' '.join(strip_tags(self.address).split())

        self.full_clean()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    class Meta:
        verbose_name = 'Profile'
        ordering = ['user']

    def __str__(self):
        return f"Profile of {self.user.username}"
