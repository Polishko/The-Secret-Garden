from django.core.exceptions import ValidationError

from thesecretgarden.common.forms import ProductBaseForm
from thesecretgarden.flowers.models import Plant


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


class PlantBulkCreateForm(PlantBaseForm):
    pass

