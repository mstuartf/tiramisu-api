from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import Template, TemplateSection, TemplateStyle, TemplateSectionType


class ReadTemplateSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateSection
        fields = (
            "id",
            "type",
            "order",
            "meta",
        )


class ReadTemplateSerializer(serializers.ModelSerializer):
    shared = serializers.SerializerMethodField()
    sections = ReadTemplateSectionSerializer(many=True)

    class Meta:
        model = Template
        fields = (
            "id",
            "name",
            "style",
            "shared",
            "sections",
            "meta",
        )

    def get_shared(self, obj):
        return obj.user is None


class WriteTemplateSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateSection
        fields = (
            "type",
            "order",
            "meta",
        )


class WriteTemplateSerializer(WritableNestedModelSerializer):
    sections = WriteTemplateSectionSerializer(many=True)

    class Meta:
        model = Template
        fields = ("name", "style", "meta", "sections", "user")


class ReadTemplateStyleSerializer(serializers.ModelSerializer):

    class Meta:
        model = TemplateStyle
        fields = "__all__"


class ReadTemplateSectionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TemplateSectionType
        fields = "__all__"
