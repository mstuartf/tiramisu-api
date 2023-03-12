from rest_framework import serializers

from .models import CustomUser


class ReadUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "admin",
        )