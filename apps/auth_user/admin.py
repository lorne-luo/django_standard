from django.contrib import admin
from django import forms

from .models import User


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser',
                    'date_joined']
    readonly_fields = ['password', 'date_joined', 'is_superuser']


admin.site.register(User, UserAdmin)
