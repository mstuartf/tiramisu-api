from rest_framework import serializers

from .models import CustomUser


class ReadUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "admin",
            "company",
            "linkedin_tracking_enabled",
            "msg_tracking_activated",
            "like_tracking_activated",
            "comment_tracking_activated",
            "auto_save",
            "openai_model",
        )
