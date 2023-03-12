from rest_framework import serializers

from .models import Prompt


class ReadPromptSerializer(serializers.ModelSerializer):
    custom = serializers.SerializerMethodField()

    class Meta:
        model = Prompt
        fields = (
            "id",
            "name",
            "text",
            "custom",
        )

    def get_custom(self, obj):
        return obj.user is not None


class WritePromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ("name", "text", "user")

