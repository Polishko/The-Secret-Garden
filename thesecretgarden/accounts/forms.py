from datetime import date

from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import DateInput

from thesecretgarden.accounts.models import Profile
from thesecretgarden.mixins import PlaceHolderMixin

UserModel = get_user_model()

class AppUserCreateForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a password of at least 8 characters with both letters and numbers.'
        }),
        label="Password",
        )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        label="Confirm Password",
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email',)

        error_messages = {
            'username': {
                'unique': "This username is already taken. Please choose another one.",
            },
            'email': {
                'unique': "This email address is already registered.",
            },
        }

        labels = {
            'username': 'User Name',
            'email': 'Email Address',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a unique username.'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter a valid email address.'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserModel.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email address is already registered.")
        return email.lower()

class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel
        fields = ('username', 'email', 'role', 'is_staff', 'is_active')

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if UserModel.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This username is already taken. Please choose another one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if UserModel.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email address is already registered.")
        return email

class AppUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username',
        }),
        label="Username",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
        }),
        label="Password",
    )

    error_messages = {
        'invalid_login': "Please enter a correct username and password. Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive. Please contact support.",
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            user = None

        if user and not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

        self.user_cache = authenticate(self.request, username=username, password=password)
        if self.user_cache is None:
            raise self.get_invalid_login_error()

        return self.cleaned_data


class ProfileEditForm(PlaceHolderMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'preferred_flower_type', 'address', 'phone', 'birthday']
        widgets = {
            'birthday': DateInput(attrs={
                'type': 'date',
                'max': date.today().isoformat(),
            }),
        }

