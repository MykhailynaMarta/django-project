from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django import forms
from django.conf import settings

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", "phone_number", "user_role"]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'user_role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'user_role')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)