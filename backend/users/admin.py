from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserModel(UserAdmin):
    model = CustomUser
    list_diasplay = ['username', 'email', 'is_staff']


admin.site.register(CustomUser, CustomUserModel)
