from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["id", "email", "company__name", "admin", "linkedin_tracking_enabled"]
    ordering = ('email',)

    fieldsets = (
        (None, {"fields": ("email", "password", "company")}),
        ("Permissions", {"fields": ("is_staff", "is_active",)}),
        ("Flags", {"fields": ("linkedin_tracking_enabled",)}),
        ("Config", {"fields": ("msg_tracking_activated", "like_tracking_activated", "comment_tracking_activated", "admin",)}),
    )

    def company__name(self, obj):
        return obj.company.name if obj.company else None


admin.site.register(CustomUser, CustomUserAdmin)
