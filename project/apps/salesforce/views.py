import logging

from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .auth import get_tokens
from .models import Credentials
from ..companies.models import Company

logger = logging.getLogger(__name__)

# https://login.salesforce.com/services/oauth2/authorize?response_type=code&client_id=3MVG9DREgiBqN9Wkw5rCCuprOH4CNQc7xTCWA_5GEP5NE3ndthkvZIS.yT4KNLG534DyflKVNtN1HuktVRWWm&redirect_uri=$ORIGIN/salesforce/oauth/callback&state=$COMPANY_ID

@api_view()
@permission_classes((AllowAny, ))
def oauth_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    company = Company.objects.get(pk=state)
    tokens = get_tokens(code)
    tokens.pop('id')

    try:
        logger.info('looking for existing credentials for company')
        Credentials.objects.get(company=company)
        Credentials.objects.filter(company=company).update(**tokens)
    except Credentials.DoesNotExist:
        logger.info('creating new credentials')
        Credentials.objects.create(company=company, **tokens)

    return HttpResponse('ok')
