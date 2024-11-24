from django import forms


class ProductBaseForm(forms.ModelForm):
    class Meta:
        exclude = ('slug',)
        widgets = {
            'price': forms.NumberInput(attrs={
                'step': '0.01',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'DELETE' in self.fields:
            self.fields['DELETE'].label = 'Disable form if not needed'
