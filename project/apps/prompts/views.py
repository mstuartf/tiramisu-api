import logging

from django.db.models import Q
from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from .models import Prompt
from .serializers import (
    WritePromptSerializer,
    ReadPromptSerializer,
)

logger = logging.getLogger(__name__)


class PromptView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):

    serializer_class = ReadPromptSerializer

    def get_queryset(self):
        return Prompt.objects.filter(Q(user=None) | Q(user=self.request.user))

    def create(self, request, *args, **kwargs):
        data = {
            **request.data,
            "user": request.user.id,
        }
        serializer = WritePromptSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        read_serializer = ReadPromptSerializer(obj)
        headers = self.get_success_headers(read_serializer.data)
        return Response(
            read_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
