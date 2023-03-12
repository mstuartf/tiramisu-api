from django.db import models
from api.models import RootModel
from ..accounts.models import CustomUser
from ..prompts.models import Prompt
from ..prospects.models import Prospect


class MessageSet(RootModel):
    raw = models.JSONField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)


class Message(RootModel):
    set = models.ForeignKey(MessageSet, on_delete=models.CASCADE, related_name="messages")
    raw = models.JSONField()
    parsed = models.TextField()
    copied = models.BooleanField(default=False)
