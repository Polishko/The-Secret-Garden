from django.core.exceptions import ValidationError

from thesecretgarden.common.forms import ProductBaseForm
from thesecretgarden.gifts.models import Gift
from thesecretgarden.mixins import DisableFieldMixin


class GiftBaseForm(ProductBaseForm):
    class Meta(ProductBaseForm.Meta):
        model = Gift
        fields = ['brand_name', 'short_name', 'type', 'photo', 'price', 'stock', 'short_description']
        error_messages = {
            'type': {
                'invalid_choice': 'Please select a valid type!',
                'required': 'Please select a type!',
            },
        }

    def clean_brand_name(self):
        brand_name = self.cleaned_data.get('brand_name')

        if Gift.objects.filter(brand_name=brand_name).exclude(pk=self.instance.pk).exists():
            raise ValidationError('A gift with this name already exists.')

        return brand_name

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            valid_mime_types = ['image/jpeg', 'image/png', 'image/gif']
            if photo.content_type not in valid_mime_types:
                raise ValidationError("Unsupported file type. Please upload a valid image file (JPEG, PNG, GIF).")
        return photo


class GiftBulkCreateForm(GiftBaseForm):
    pass


class GiftCreateForm(GiftBaseForm):
    pass

class GiftEditForm(GiftBaseForm):
    pass

class GiftDeleteForm(DisableFieldMixin, GiftBaseForm):
    readonly_fields = ['brand_name', 'short_name', 'type', 'photo', 'price', 'stock', 'short_description']
