import re
import json
import logging

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .chat import draft_completion_messages, draft_chat_messages
from .prompt import build_prompt, build_chat_messages

from ..prompts.models import Prompt
from ..templates.models import Template
from ..prospects.models import Prospect

from .serializers import (
    WriteMessageSetSerializer,
    ReadMessageSetSerializer,
    WriteMessageSerializer,
)

from .models import Message
from ..prospects.serializers import WriteProspectSerializer

logger = logging.getLogger(__name__)


# completion = {
#     "choices": [
#         {
#             "text": ":\n\n1. \"Looks like you're the go-to guy for start-ups needing help with sales and lead gen!\"\n2. You must be a pro at email marketing - I'm sure you know all the tricks of the trade!\n3.\"Account management is a tricky business - glad you've got it covered!\"\n\"Contact centers don't stand a chance against you and your business development expertise!\"\nYou must be in high demand with all the skills you've got!"
#         }
#     ],
# }

def parse_numbered_messages(raw_messages):
    messages = []
    for msg in raw_messages:
        match = re.match(r'(\d\.)( *")?([^"]+)"?', msg)
        if not match:
            continue

        parsed = match.groups()[2].strip()
        if len(parsed) < 2:
            continue
        logger.info(parsed)
        messages.append({
            "parsed": parsed,
        })
    return messages


# todo: REMOVE_V1
def get_instances_v1(request):
    logger.info("generating messages for prompt {} to prospect {}".format(
        request.data["prompt"],
        request.data["prospect"],
    ))
    prompt = Prompt.objects.get(pk=request.data["prompt"])
    prospect = Prospect.objects.get(pk=request.data["prospect"])
    return prospect, prompt


def get_instances_v2(request):
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
    return prospect, prompt


def get_instances_v3(request):
    template_id = request.data["template_id"]
    prospect_data = request.data["profile"]
    logger.info("generating messages for templaet {} to prospect {}".format(
        template_id,
        prospect_data["slug"],
    ))
    template = Template.objects.get(pk=template_id)
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
    return prospect, template


class MessageSetView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = ReadMessageSetSerializer

    def create(self, request, *args, **kwargs):
        # prompt,prospect
        if request.data.get("prospect"):
            prospect, prompt = get_instances_v1(request)
            full_prompt = build_prompt(prompt, prospect)
            args = {"prompt": prompt.id}
            raw = draft_completion_messages(full_prompt)
            raw_messages = raw["choices"][0]["text"].split("\n")
            messages = parse_numbered_messages(raw_messages)

        # prompt_id, profile
        elif request.data.get("prompt_id"):
            prospect, prompt = get_instances_v2(request)
            full_prompt = build_prompt(prompt, prospect)
            args = {"prompt": prompt.id}
            raw = draft_completion_messages(full_prompt)
            raw_messages = raw["choices"][0]["text"].split("\n")
            messages = parse_numbered_messages(raw_messages)

        # template_id, profile
        else:
            prospect, template = get_instances_v3(request)
            chat_messages = build_chat_messages(template, prospect)
            args = {"template": template.id}
            raw = draft_chat_messages(chat_messages)
            raw_messages = raw["choices"][0]["message"]["content"]
            logger.info(raw_messages)
            messages = [{"parsed": m["message"]} for m in json.loads(raw_messages)]

        data = {
            "user": request.user.id,
            "prospect": prospect.id,
            "raw": raw,
            "messages": messages,
            **args,
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
