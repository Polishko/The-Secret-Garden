from django import forms
from django.core.exceptions import ValidationError

from thesecretgarden.flowers.models import Plant


class PlantBaseForm(forms.ModelForm):
    class Meta:
        model = Plant
        exclude = ('slug',)
        widgets = {
            'price': forms.NumberInput(attrs={
                'step': '0.01',
            }),
        }
        error_messages = {
            'type': {
                'invalid_choice': 'Please select a valid type!',
                'required': 'Please select a type!',
            },
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # if hasattr(self, 'fields'):
            if 'DELETE' in self.fields:
                self.fields['DELETE'].label = 'Disable form if not needed'



    def clean_name(self):
        name = self.cleaned_data.get('name')

        if Plant.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise ValidationError('A plant with this name already exists.')

        return name


class PlantBulkCreateForm(PlantBaseForm):
    pass

