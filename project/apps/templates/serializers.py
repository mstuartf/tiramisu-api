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
    sections = ReadTemplateSectionSerializer(many=True)

    class Meta:
        model = Template
        fields = (
            "id",
            "name",
            "style",
            "sections",
            "meta",
            "user",
        )


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
