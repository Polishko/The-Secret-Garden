from cloudinary.exceptions import Error
from cloudinary.uploader import upload
from django.core.exceptions import ValidationError

from django.core.files.uploadedfile import InMemoryUploadedFile

from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.utils.html import strip_tags

from thesecretgarden.common.models import Product


class Plant(Product):
    PLANT_CHOICES = [
        ('non-floral', 'Non Floral Plants'),
        ('floral', 'Floral Plants'),
        ('cactus', 'Cactus'),
    ]

    type = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        choices=PLANT_CHOICES,
        default='floral',
        verbose_name='Type',
        help_text='Provide plant type.',
    )

    description = models.TextField(
        null=False,
        blank=False,
        validators=(
            MinLengthValidator(10, message="Description should be at least 10 characters."),
            MaxLengthValidator(300, message="Description should not exceed 300 characters."),
        ),
        verbose_name='Description',
        help_text = 'Provide a description for the plant product.'
    )

    def save(self, *args, **kwargs):
        if self.description:
            self.description = ' '.join(strip_tags(self.description).split())

        if self.photo and isinstance(self.photo, InMemoryUploadedFile):
            try:
                # Handle new photo uploads
                upload_result = upload(
                    self.photo,  # Pass the file to Cloudinary
                )
                # Assign the public_id to the CloudinaryField
                self.photo = upload_result['public_id']
            except Error as e:
                raise ValidationError(f"Invalid file type: {str(e)}")

        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Plant'

    def __str__(self):
        return f'Plant: {self.name} ({self.type})'
