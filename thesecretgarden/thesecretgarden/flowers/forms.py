from django.core.exceptions import ValidationError

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
            valid_mime_types = ['image/jpeg', 'image/png', 'image/gif']
            if photo.content_type not in valid_mime_types:
                raise ValidationError("Unsupported file type. Please upload a valid image file (JPEG, PNG, GIF).")
        return photo


class PlantBulkCreateForm(PlantBaseForm):
    pass

class PlantCreateForm(PlantBaseForm):
    pass

class PlantEditForm(PlantBaseForm):
    pass

class PlantDeleteForm(DisableFieldMixin, PlantBaseForm):
    readonly_fields = ['name', 'price', 'type', 'stock', 'description', 'photo']
