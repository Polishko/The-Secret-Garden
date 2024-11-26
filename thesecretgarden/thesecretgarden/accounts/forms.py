from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError

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
