from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

class CustomAuthForm(AuthenticationForm):
    username = forms.EmailField(label = ('Email Address'),
                                max_length=256,
                                widget=forms.EmailInput(attrs={'autofocus': True}),
                            )
    password = forms.CharField(label=('password'),
                               strip=False,
                               widget=forms.PasswordInput,
                            )