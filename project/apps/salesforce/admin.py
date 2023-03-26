from django.contrib import admin
from .models import Credentials


@admin.register(Credentials)
class CredentialsAdmin(admin.ModelAdmin):
    model = Credentials

    list_display = (
        "id",
        "company__name"
    )

    def company__name(self, obj):
        return obj.company.name
