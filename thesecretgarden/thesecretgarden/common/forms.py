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


class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        required=False,
        error_messages= {
            'max_length': 'You can only enter 100 characters!'
        },
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for a product...'
            }
        )
    )
