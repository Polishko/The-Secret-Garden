from cloudinary import CloudinaryResource
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from thesecretgarden.common.forms import ProductBaseForm
from thesecretgarden.flowers.models import Plant
from thesecretgarden.mixins import DisableFieldMixin


class PlantBaseForm(ProductBaseForm):
    class Meta(ProductBaseForm.Meta):
        model = Plant
        error_messages = {
            'type': {
                'invalid_choice': 'Please select a valid type!',
                'required': 'Please select a type!',
            },
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if Plant.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise ValidationError('A plant with this name already exists.')

        return name

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        if photo:
            if isinstance(photo, (InMemoryUploadedFile, TemporaryUploadedFile)):
                valid_mime_types = ['image/jpeg', 'image/png', 'image/gif']
                if photo.content_type not in valid_mime_types:
                    raise ValidationError("Unsupported file type. Please upload a valid image file (JPEG, PNG, GIF).")
            elif isinstance(photo, CloudinaryResource):
                pass
            else:
                print(f"Unsupported photo type: {type(photo)}, content: {photo}")
                raise ValidationError("Unsupported photo type.")
        return photo

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')

        if self.instance.pk:
            reserved_stock = self.instance.stock - self.instance.get_available_stock()
            if stock < reserved_stock:
                raise ValidationError(
                    f"Stock cannot be less than reserved stock ({reserved_stock})."
                )
        return stock


class PlantBulkCreateForm(PlantBaseForm):
    pass

class PlantCreateForm(PlantBaseForm):
    pass

class PlantEditForm(PlantBaseForm):
    pass

class PlantDeleteForm(DisableFieldMixin, PlantBaseForm):
    readonly_fields = ['name', 'price', 'type', 'stock', 'description', 'photo']
