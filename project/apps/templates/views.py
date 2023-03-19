import logging

from django.db.models import Q
from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from .models import Template, TemplateStyle, TemplateSectionType
from .serializers import (
    WriteTemplateSerializer,
    ReadTemplateSerializer,
    ReadTemplateStyleSerializer,
    ReadTemplateSectionTypeSerializer,
)

logger = logging.getLogger(__name__)


class TemplateView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):

    serializer_class = ReadTemplateSerializer

    def get_queryset(self):
        return Template.objects.filter(Q(user=None) | Q(user=self.request.user))

    def create(self, request, *args, **kwargs):
        data = {
            **request.data,
            "user": request.user.id,
        }
        serializer = WriteTemplateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        read_serializer = ReadTemplateSerializer(obj)
        headers = self.get_success_headers(read_serializer.data)
        return Response(
            read_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        logger.info(request.data)
        data = {
            **request.data,
            "user": request.user.id,
        }
        instance = self.get_object()
        serializer = WriteTemplateSerializer(instance, data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        read_serializer = ReadTemplateSerializer(instance)
        headers = self.get_success_headers(read_serializer.data)
        return Response(
            read_serializer.data, status=status.HTTP_200_OK, headers=headers
        )


class TemplateStyleView(
    mixins.ListModelMixin,
    GenericViewSet,
):

    serializer_class = ReadTemplateStyleSerializer
    queryset = TemplateStyle.objects.all()


class TemplateSectionTypeView(
    mixins.ListModelMixin,
    GenericViewSet,
):

    serializer_class = ReadTemplateSectionTypeSerializer
    queryset = TemplateSectionType.objects.all()
