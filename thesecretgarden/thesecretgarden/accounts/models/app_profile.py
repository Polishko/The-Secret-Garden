from django.core.exceptions import ValidationError
from django.utils import timezone

from django.db import models
from django.contrib.auth import get_user_model

from thesecretgarden.accounts.validators import NameValidator

UserModel = get_user_model()


class Profile(models.Model):
    FLOWER_CHOICES = (
        ('non-floral', 'Non Floral Plants'),
        ('floral', 'Floral Plants'),
        ('cactus', 'Cactuses'),
    )

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

    created_at = models.DateTimeField(default=timezone.now, editable=False)

    preferred_flower_type = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=FLOWER_CHOICES,
        verbose_name='Preferred Flower Type',
    )

    def clean(self):
        if self.first_name == self.last_name:
            raise ValidationError('First name and last name cannot be the same!')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Profile'
        ordering = ['user']
