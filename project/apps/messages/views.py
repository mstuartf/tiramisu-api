import logging

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .chat import draft_messages
from .prompt import build_prompt

from ..prompts.models import Prompt
from ..prospects.models import Prospect

from .serializers import (
    WriteMessageSetSerializer,
    ReadMessageSetSerializer,
)

logger = logging.getLogger(__name__)


class MessageSetView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):

    serializer_class = ReadMessageSetSerializer

    # {
    #     "prompt": "bcd5dbd1-2916-4529-80ea-e4f054fab718",
    #     "prospect": "7c43b77c-6dad-471f-b276-e5d3a27861f0"
    # }

    def create(self, request, *args, **kwargs):
        logger.info("generating messages for prompt {} to prospect {}".format(
            request.data["prompt"],
            request.data["prospect"],
        ))
        prompt = Prompt.objects.get(pk=request.data["prompt"])
        prospect = Prospect.objects.get(pk=request.data["prospect"])
        messages = draft_messages(build_prompt(prompt, prospect))
        choices = messages.pop("choices")
        logger.info(messages)
        data = {
            "user": request.user.id,
            "prospect": prospect.id,
            "prompt": prompt.id,
            "raw": messages,
            "messages": [
                {
                    "raw": raw,
                    "parsed": raw["text"]
                } for raw in choices
            ]
        }
        serializer = WriteMessageSetSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        read_serializer = ReadMessageSetSerializer(obj)
        headers = self.get_success_headers(read_serializer.data)
        return Response(
            read_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
