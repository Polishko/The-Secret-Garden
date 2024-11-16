from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import TextInput, EmailInput

UserModel = get_user_model()

class AppUserForm(UserCreationForm):
    """
    Form for creating new users in the admin panel
    """
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email',)
        help_texts = {
            'username': 'Enter a unique username.',
            'email': 'Enter a valid email address.',
        }
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
            'username': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
        }

class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel
        fields = ('username', 'email', 'role', 'is_staff', 'is_active')
