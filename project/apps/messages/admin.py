from django.contrib import admin
from .models import MessageSet, Message, LinkedInMessage


@admin.register(MessageSet)
class MessageSetAdmin(admin.ModelAdmin):
    model = MessageSet

    list_display = (
        "id",
        "prospect__slug",
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
        "set__id",
    )
    def set__prospect__slug(self, obj):
        return obj.set.prospect.slug

    def set__user__email(self, obj):
        return obj.set.user.email

    def set__id(self, obj):
        return obj.set.id


@admin.register(LinkedInMessage)
class LinkedInMessageAdmin(admin.ModelAdmin):
    model = LinkedInMessage

    list_display = (
        "id",
        "profile_slug",
        "profile_name",
        "user__email",
    )
    def user__email(self, obj):
        return obj.user.email
