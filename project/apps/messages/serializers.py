from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import MessageSet, Message


class ReadMessageSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "text",
        )

    def get_text(self, obj):
        return obj.parsed


class ReadMessageSetSerializer(serializers.ModelSerializer):
    messages = ReadMessageSerializer(many=True)

    class Meta:
        model = MessageSet
        fields = (
            "id",
            "prospect_id",
            "prompt_id",
            "messages",
        )


class WriteMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            "raw",
            "parsed",
            "copied"
        )


class WriteMessageSetSerializer(WritableNestedModelSerializer):
    messages = WriteMessageSerializer(many=True)

    class Meta:
        model = MessageSet
        fields = (
            "user",
            "prospect",
            "prompt",
            "raw",
            "messages",
        )
