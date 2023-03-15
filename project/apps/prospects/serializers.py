from rest_framework import serializers

from .models import Prospect


# todo: REMOVE_V1
class ReadProspectSerializerOld(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

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

    def get_first_name(self, obj):
        return obj.full_name

    def get_last_name(self, obj):
        return None


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
