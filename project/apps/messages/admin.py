from django.contrib import admin
from .models import MessageSet, Message


@admin.register(MessageSet)
class MessageSetAdmin(admin.ModelAdmin):
    model = MessageSet

    list_display = (
        "id",
        "prospect__slug",
        "prompt__name",
        "user__email",
        "user__company__name",
        "nb_messages",
    )

    list_filter = (
        'user__company__name',
        'user__email',
    )

    def prospect__slug(self, obj):
        return obj.prospect.slug

    def prompt__name(self, obj):
        return obj.prompt.name

    def user__email(self, obj):
        return obj.user.email

    def user__company__name(self, obj):
        return obj.user.company.name if obj.user.company else None

    def nb_messages(self, obj):
        return obj.messages.count()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message

    list_display = (
        "id",
        "set__prospect__slug",
        "set__user__email",
        "parsed",
        "copied",
    )
    def set__prospect__slug(self, obj):
        return obj.set.prospect.slug

    def set__user__email(self, obj):
        return obj.set.user.email
