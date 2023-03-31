import os

from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company

    list_display = (
        "id",
        "name",
        "salesforce_link",
    )

    def salesforce_link(self, obj):
        return 'https://login.salesforce.com/services/oauth2/authorize?response_type=code&client_id=' \
               '{client_id}&redirect_uri={redirect_uri}&state={state}'.format(
            client_id=os.environ["SALESFORCE_CONSUMER_KEY"],
            redirect_uri=os.environ["SALESFORCE_CALLBACK_URL"],
            state=str(obj.id),
        )
