from django.contrib import admin
from .models import Credentials, Task


@admin.register(Credentials)
class CredentialsAdmin(admin.ModelAdmin):
    model = Credentials

    list_display = (
        "id",
        "company__name"
    )

    def company__name(self, obj):
        return obj.company.name


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    model = Task

    list_display = (
        "id",
        "task_id",
        "user__email"
    )

    def user__email(self, obj):
        return obj.msg.user.email
