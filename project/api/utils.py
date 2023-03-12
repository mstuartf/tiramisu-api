from django.test import TransactionTestCase
from rest_framework.test import APIClient


class EndpointTestCase(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()

    def loginAs(self, user):
        self.client.force_login(user, "django.contrib.auth.backends.ModelBackend")
