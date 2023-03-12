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
        "nb_messages",
    )
    def prospect__slug(self, obj):
        return obj.prospect.slug

    def prompt__name(self, obj):
        return obj.prompt.name

    def user__email(self, obj):
        return obj.user.email

    def nb_messages(self, obj):
        return obj.messages.count()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message

    list_display = (
        "id",
        "parsed",
        "copied",
    )
