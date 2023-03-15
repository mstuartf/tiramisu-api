from django.contrib import admin
from .models import Prospect


@admin.register(Prospect)
class ProspectAdmin(admin.ModelAdmin):
    model = Prospect

    list_display = (
        "id",
        "slug",
        "full_name",
        "user__email",
        "user__company__name",
    )

    list_filter = (
        'user__company__name',
        'user__email',
    )

    def user__email(self, obj):
        return obj.user.email if obj.user else None

    def user__company__name(self, obj):
        return obj.user.company.name if (obj.user and obj.user.company) else None
