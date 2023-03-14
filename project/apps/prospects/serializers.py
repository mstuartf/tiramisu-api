from rest_framework import serializers

from .models import Prospect


class ReadProspectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prospect
        fields = (
            "id",
            "full_name",
            "headline",
            "talks_about",
            "summary",
            "slug",
        )


class WriteProspectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prospect
        fields = (
            "slug",
            "full_name",
            "headline",
            "talks_about",
            "summary",
            "user",
        )
