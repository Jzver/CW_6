from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from utils.forms_mixins import StyleFormMixin
from django import forms

class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'avatar', 'token')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['token'].widget = forms.HiddenInput()

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'avatar', 'token')

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['token'].widget = forms.HiddenInput()

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
