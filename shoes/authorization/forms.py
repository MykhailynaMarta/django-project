from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import PasswordInput, TextInput
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    widgets = {
        "user_name": TextInput(attrs={'placeholder': 'ex:test', 'autocomplete': 'off'}),
        "password": PasswordInput(attrs={'placeholder': '********', 'autocomplete': 'off', 'data-toggle': 'password'}),
    }


class CustomUserChangeForm(UserChangeForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = CustomUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if not field.required:
                field.required = False

    widgets = {
        "user_name": TextInput(attrs={'placeholder': 'ex:test', 'autocomplete': 'off'}),
        "password": PasswordInput(attrs={'placeholder': '********', 'autocomplete': 'off', 'data-toggle': 'password'}),
    }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()

