import cloudinary.uploader
from cloudinary.uploader import upload
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.utils.html import strip_tags

from thesecretgarden.common.models import Product
from thesecretgarden.flowers.validators import PlantDescriptionValidator


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
            PlantDescriptionValidator(),
            MinLengthValidator(10, message='Description should be at least 10 characters.'),
            MaxLengthValidator(300, message='Description should not exceed 1000 characters.'),
        ),
        verbose_name='Description',
        help_text = 'Provide a description for the plant product.'
    )

    def save(self, *args, **kwargs):
        if self.description:
            self.description = ' '.join(strip_tags(self.description).split())

        if self.photo and isinstance(self.photo.file, InMemoryUploadedFile):
            upload_result = upload(
                self.photo.file,  # Pass the file to Cloudinary
            )
            # Assign the public_id to the CloudinaryField
            self.photo = upload_result['public_id']

        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Plant'

    def __str__(self):
        return f'Plant: {self.name} ({self.type})'
