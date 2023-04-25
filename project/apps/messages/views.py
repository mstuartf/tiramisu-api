import logging

from django.db.models import Count
from django.shortcuts import render
from rest_framework import mixins, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Message, MessageSet, LinkedInMessage, LinkedInLike, LinkedInComment
from .serializers import (
    BaseMessageSetSerializer,
    ReadMessageSetSerializer,
    WriteMessageSerializer,
    WriteLinkedInMessageSerializer, ReadLinkedInMessageSerializer,
    WriteLinkedInLikeSerializer, ReadLinkedInLikeSerializer,
    WriteLinkedInCommentSerializer, ReadLinkedInCommentSerializer,
)
from .tasks import generate_message_task
from ..companies.models import Company
from ..prospects.models import Prospect
from ..prospects.serializers import WriteProspectSerializer
from ..salesforce.tasks import create_salesforce_msg_task, create_salesforce_like_task, create_salesforce_comment_task
from ..templates.models import Template

logger = logging.getLogger(__name__)


def find_or_create_prospect(prospect_data, user):
    try:
        prospect = Prospect.objects.get(slug=prospect_data['slug'])
    except Prospect.DoesNotExist:
        logger.info("no profile in db with this slug, creating")
        data = {
            "user": user.id,
            **prospect_data,
        }
        serializer = WriteProspectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        prospect = serializer.save()

    return prospect


class MessageSetView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = ReadMessageSetSerializer

    def get_queryset(self):
        return MessageSet.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.error is not None:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        template_id = request.data["template_id"]
        prospect_data = request.data["profile"]
        logger.info("generating messages for template {} to prospect {}".format(
            template_id,
            prospect_data["slug"],
        ))
        template = Template.objects.get(pk=template_id)
        prospect = find_or_create_prospect(prospect_data, request.user)

        data = {
            "user": request.user.id,
            "prospect": prospect.id,
            "template": template.id,
        }

        serializer = BaseMessageSetSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            logger.info(e)
            raise

        obj = serializer.save()

        logger.info('deferring msg task')
        generate_message_task.apply_async(args=[str(obj.id)])

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


class LinkedInMessageView(
    mixins.CreateModelMixin,
    GenericViewSet,
):
    serializer_class = WriteLinkedInMessageSerializer

    def get_queryset(self):
        return LinkedInMessage.objects.filter(set__user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = {
            **request.data,
            "user": request.user.id,
        }
        serializer = WriteLinkedInMessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        create_salesforce_msg_task.apply_async(args=[str(obj.id)])
        read_serializer = ReadLinkedInMessageSerializer(obj)
        headers = self.get_success_headers(read_serializer.data)
        return Response(
            read_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class LinkedInLikeView(
    mixins.CreateModelMixin,
    GenericViewSet,
):
    serializer_class = WriteLinkedInLikeSerializer

    def get_queryset(self):
        return LinkedInLike.objects.filter(set__user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = {
            **request.data,
            "user": request.user.id,
        }
        serializer = WriteLinkedInLikeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        create_salesforce_like_task.apply_async(args=[str(obj.id)])
        read_serializer = ReadLinkedInLikeSerializer(obj)
        headers = self.get_success_headers(read_serializer.data)
        return Response(
            read_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class LinkedInCommentView(
    mixins.CreateModelMixin,
    GenericViewSet,
):
    serializer_class = WriteLinkedInCommentSerializer

    def get_queryset(self):
        return LinkedInComment.objects.filter(set__user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = {
            **request.data,
            "user": request.user.id,
        }
        serializer = WriteLinkedInCommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        create_salesforce_comment_task.apply_async(args=[str(obj.id)])
        read_serializer = ReadLinkedInCommentSerializer(obj)
        headers = self.get_success_headers(read_serializer.data)
        return Response(
            read_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


@permission_classes((AllowAny, ))
def activity_view(request, company_id=None):
    company = Company.objects.get(pk=company_id)
    users = company.customuser_set.all().annotate(
        nb_messages=Count('linkedinmessage', distinct=True),
        nb_likes=Count('linkedinlike', distinct=True),
        nb_comments=Count('linkedincomment', distinct=True),
    )
    return render(request, 'activity.html', {'users': users, 'company': company})
