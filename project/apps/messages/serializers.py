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
            "messages",
            "processed",
        )


class WriteMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            "parsed",
            "copied"
        )


class BaseMessageSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageSet
        fields = (
            "user",
            "prospect",
            "template",
        )


class WriteMessageSetSerializer(WritableNestedModelSerializer):
    messages = WriteMessageSerializer(many=True)

    class Meta:
        model = MessageSet
        fields = (
            "user",
            "prospect",
            "template",
            "raw",
            "messages",
            "processed",
        )
