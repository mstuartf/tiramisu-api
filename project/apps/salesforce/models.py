from django.db import models
from api.models import RootModel
from ..companies.models import Company
from..messages.models import LinkedInMessage


class Credentials(RootModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    signature = models.TextField()
    scope = models.TextField()
    id_token = models.TextField()
    instance_url = models.TextField()
    token_type = models.TextField()
    issued_at = models.TextField()


class Task(RootModel):
    msg = models.ForeignKey(LinkedInMessage, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=255)
