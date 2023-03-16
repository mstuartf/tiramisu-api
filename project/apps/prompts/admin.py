from django.contrib import admin
from .models import Prompt


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    model = Prompt

    list_display = (
        "id",
        "user__email",
        "name",
        "text",
        "deprecated",
    )

    def user__email(self, obj):
        return obj.user.email if obj.user else None
