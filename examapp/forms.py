from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, ModelChoiceField
from django.db import transaction



class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.email = self.cleaned_data['email']
        user.username = user.email
        user.save()
        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'description', 'platform', 'genre', 'price', 'number_in_stock']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }
