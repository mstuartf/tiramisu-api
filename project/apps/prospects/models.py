from django.db import models
from api.models import RootModel
from ..accounts.models import CustomUser


class Prospect(RootModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    full_name = models.CharField(max_length=255)
    headline = models.TextField()
    summary = models.TextField(null=True, blank=True)
    talks_about = models.TextField(null=True, blank=True)
