import re
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
    WriteMessageSerializer,
)

from .models import Message
from ..prospects.serializers import WriteProspectSerializer

logger = logging.getLogger(__name__)


class MessageSetView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):

    serializer_class = ReadMessageSetSerializer

    def create(self, request, *args, **kwargs):
        prompt_id = request.data["prompt_id"]
        prospect_data = request.data["profile"]
        logger.info("generating messages for prompt {} to prospect {}".format(
            prompt_id,
            prospect_data["slug"],
        ))
        prompt = Prompt.objects.get(pk=prompt_id)
        try:
            prospect = Prospect.objects.get(slug=prospect_data["slug"])
        except Prospect.DoesNotExist:
            logger.info("no profile in db with this slug, creating")
            data = {
                "user": request.user.id,
                **prospect_data,
            }
            serializer = WriteProspectSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            prospect = serializer.save()

        full_prompt = build_prompt(prompt, prospect)
        logger.info(full_prompt)
        completion = draft_messages(build_prompt(prompt, prospect))
        raw_messages = completion["choices"][0]["text"].split("\n")
        messages = []
        for msg in raw_messages:
            match = re.match('(\d\.)(.+)', msg)
            if not match:
                continue

            messages.append({
                "parsed": match.groups()[1].strip(),
            })

        data = {
            "user": request.user.id,
            "prospect": prospect.id,
            "prompt": prompt.id,
            "raw": completion,
            "messages": messages,
        }
        serializer = WriteMessageSetSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        read_serializer = ReadMessageSetSerializer(obj)
        headers = self.get_success_headers(read_serializer.data)
        return Response(
            read_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class MessageView(
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = WriteMessageSerializer

    def get_queryset(self):
        return Message.objects.filter(set__user=self.request.user)
