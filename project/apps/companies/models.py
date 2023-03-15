from django.db import models
from api.models import RootModel


class Company(RootModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
