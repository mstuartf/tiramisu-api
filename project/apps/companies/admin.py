from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company

    list_display = (
        "id",
        "name",
    )
