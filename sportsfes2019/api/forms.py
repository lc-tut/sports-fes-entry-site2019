from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserCreateForm(UserCreationForm):


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "name", "gender", "phone"
        )