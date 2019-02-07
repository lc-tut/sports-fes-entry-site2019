from django.contrib import admin
from .models import User
from django.contrib.auth.models import User as BaseUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .forms import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['number', 'username', 'email']

admin.site.register(User, CustomUserAdmin)