import uuid
from django.db import models

# https://stackoverflow.com/a/28469575/15793866
# https://docs.djangoproject.com/en/dev/ref/models/fields/#uuidfield
class RootModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
