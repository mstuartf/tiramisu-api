import logging

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import (
    WriteProspectSerializer,
    ReadProspectSerializer,
)

logger = logging.getLogger(__name__)


class ProspectView(
    mixins.CreateModelMixin,
    GenericViewSet,
):

    serializer_class = ReadProspectSerializer

    def create(self, request, *args, **kwargs):
        data = {
            **request.data,
            "user": request.user.id,
            "raw": {},
        }
        serializer = WriteProspectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        read_serializer = ReadProspectSerializer(obj)
        headers = self.get_success_headers(read_serializer.data)
        return Response(
            read_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
