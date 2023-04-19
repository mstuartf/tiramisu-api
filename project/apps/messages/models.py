from django.db import models
from api.models import RootModel
from ..accounts.models import CustomUser
from ..templates.models import Template
from ..prospects.models import Prospect


class MessageSet(RootModel):
    raw = models.JSONField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True, blank=True)
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    processed = models.BooleanField(default=False)
    error = models.TextField(null=True, blank=True)


class Message(RootModel):
    set = models.ForeignKey(MessageSet, on_delete=models.CASCADE, related_name="messages")
    parsed = models.TextField()
    copied = models.BooleanField(default=False)


class LinkedInMessage(RootModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    profile_slug = models.SlugField()
    content = models.TextField()
    profile_name = models.CharField(max_length=255)
    processed = models.BooleanField(default=False)
    error = models.TextField(null=True, blank=True)


# class LinkedInLike(RootModel):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     profile_slug = models.SlugField()
#     post_url = models.URLField()
#     post_title = models.CharField(max_length=255)
