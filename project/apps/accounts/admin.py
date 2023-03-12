from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["id", "email", "company__name", "admin"]
    ordering = ('email',)

    def company__name(self, obj):
        return obj.company.name if obj.company else None


admin.site.register(CustomUser, CustomUserAdmin)
