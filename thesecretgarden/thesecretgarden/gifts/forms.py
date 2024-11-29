from django.core.exceptions import ValidationError

from thesecretgarden.common.forms import ProductBaseForm
from thesecretgarden.gifts.models import Gift
from thesecretgarden.mixins import DisableFieldMixin


class GiftBaseForm(ProductBaseForm):
    class Meta(ProductBaseForm.Meta):
        model = Gift
        fields = ['brand_name', 'short_name', 'photo', 'price', 'stock', 'short_description']
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


class GiftBulkCreateForm(GiftBaseForm):
    pass


class GiftCreateForm(GiftBaseForm):
    pass

class GiftEditForm(GiftBaseForm):
    pass

class GiftDeleteForm(DisableFieldMixin, GiftBaseForm):
    readonly_fields = ['brand_name', 'short_name', 'photo', 'price', 'stock', 'short_description']
