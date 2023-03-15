import logging

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .models import Prospect
from .proxycurl import fetch_profile_request

from .serializers import (
    WriteProspectSerializer,
    ReadProspectSerializerOld,
)

logger = logging.getLogger(__name__)


# todo: REMOVE_V1
class ProspectView(
    mixins.CreateModelMixin,
    GenericViewSet,
):

    serializer_class = ReadProspectSerializerOld

    def create(self, request, *args, **kwargs):
        slug = request.data["slug"]
        logger.info("received request for slug {}".format(slug))
        try:
            obj = Prospect.objects.get(slug=slug)
        except Prospect.DoesNotExist:
            logger.info("no profile in db with this slug")
            raw = fetch_profile_request(slug)
            data = {
                "slug": slug,
                "user": request.user.id,
                "full_name": raw.get("full_name"),
                "headline": raw.get("headline"),
                "summary": raw.get("summary"),
            }
            serializer = WriteProspectSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()

        read_serializer = ReadProspectSerializerOld(obj)
        headers = self.get_success_headers(read_serializer.data)
        return Response(
            read_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
