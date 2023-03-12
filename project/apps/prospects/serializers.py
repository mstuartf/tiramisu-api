from rest_framework import serializers

from .models import Prospect


class ReadProspectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prospect
        fields = (
            "id",
            "first_name",
            "last_name",
            "headline",
            "summary",
            "slug",
        )


class WriteProspectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prospect
        fields = (
            "slug",
            "first_name",
            "last_name",
            "headline",
            "summary",
            "raw",
            "user",
        )
