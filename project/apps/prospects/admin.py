from django.contrib import admin
from .models import Prospect


@admin.register(Prospect)
class ProspectAdmin(admin.ModelAdmin):
    model = Prospect

    list_display = (
        "id",
        "slug",
        "first_name",
        "last_name",
        "user__email",
    )

    def user__email(self, obj):
        return obj.user.email if obj.user else None
