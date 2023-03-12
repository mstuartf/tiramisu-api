from django.db import models
from api.models import RootModel
from ..accounts.models import CustomUser


class Prompt(RootModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    text = models.TextField()
