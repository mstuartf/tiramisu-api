from django.db import models
from api.models import RootModel
from ..companies.models import Company


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
