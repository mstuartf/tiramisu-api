from django.apps import AppConfig


class MessagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    label = "openai_messages"
    name = 'apps.messages'
