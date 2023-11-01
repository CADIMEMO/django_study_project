from django import forms
from django.core import validators
from .models import Profile
from django.contrib.auth.models import Group
from django.forms import ModelForm


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = 'user', 'bio', 'avatar'
    images = forms.ImageField(
        widget=forms.ClearableFileInput({'multiple': False})
    )
