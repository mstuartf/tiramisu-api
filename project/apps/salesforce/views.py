import logging
import os
import json

import requests
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Credentials
from ..companies.models import Company

logger = logging.getLogger(__name__)

# https://login.salesforce.com/services/oauth2/authorize?response_type=code&client_id=3MVG9DREgiBqN9Wkw5rCCuprOH4CNQc7xTCWA_5GEP5NE3ndthkvZIS.yT4KNLG534DyflKVNtN1HuktVRWWm&redirect_uri=https://8b72-80-4-216-68.eu.ngrok.io/salesforce/oauth/callback&state=123abc


def get_tokens(code):
    res = requests.get(
        "https://login.salesforce.com/services/oauth2/token",
        params={
          'code': "{}".format(code),
          'grant_type': 'authorization_code',
          'client_id': os.environ['SALESFORCE_CONSUMER_KEY'],
          'client_secret': os.environ['SALESFORCE_CONSUMER_SECRET'],
          'redirect_uri': os.environ['SALESFORCE_CALLBACK_URL'],
        },
    )
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        logger.info(res.json())
        raise

    return res.json()


def salesforce_req(token, path):
    res = requests.get(
        "https://seasmokeltd-dev-ed.develop.my.salesforce.com/services/data/v57.0/sobjects/{}".format(path),
        headers={
          'Authorization': "Bearer {}".format(token),
          'Content-Type': 'application/json',
        },
    )
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        logger.info(res.json())
        raise

    return res.json()


def create_record(token, path, payload):
    res = requests.post(
        "https://seasmokeltd-dev-ed.develop.my.salesforce.com/services/data/v57.0/sobjects/{}".format(path),
        json=payload,
        headers={
          'Authorization': "Bearer {}".format(token),
          'Content-Type': 'application/json',
        },
    )
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        logger.info(res.json())
        raise

    return res.json()


def list_tasks(token):
    return salesforce_req(token, 'Task')


def get_contact(token, _id):
    return salesforce_req(token, 'Contact/{}'.format(_id))


@api_view()
@permission_classes((AllowAny, ))
def oauth_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    company = Company.objects.get(pk=state)
    tokens = get_tokens(code)
    tokens.pop('id')
    logger.info(tokens)
    Credentials.objects.create(**tokens, company=company)
    return HttpResponse('ok')


# https://MyDomainName.my.salesforce.com/services/data/vXX.X/resource/
# https://seasmokeltd-dev-ed.develop.my.salesforce.com/services/data/v57.0/task
# curl https://MyDomainName.my.salesforce.com/services/data/v57.0/sobjects/Account/ -H "Authorization Bearer access-token" -H “Content-Type: application/json” —data-binary @new-account.json -X POST


@api_view()
@permission_classes((AllowAny, ))
def test(request):
    # https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_task.htm
    # https://developer.salesforce.com/docs/atlas.en-us.sfFieldRef.meta/sfFieldRef/salesforce_field_reference_Task.htm
    credentials = Credentials.objects.first()
    res = create_record(credentials.access_token, 'Task', {
        "WhoId": "0038d00000UbgxSAAR",  # contact id goes here
        "Subject": "LinkedIn message",
        "WhatId": "0018d00000VnAK8AAN",  # account this relates to
        "Status": "Completed",
        "ActivityDate": "2023-03-26T20:17:42.000+0000",  # due date
        "Description": "Dear John, this is a LinkedIn message that I sent to you... [example]",
    })
    # res = salesforce_req(credentials.access_token, 'Task/00T8d00000vGo6KEAS')
    # res = salesforce_req(credentials.access_token, 'Activity')
    # res = salesforce_req(credentials.access_token, 'Contact/0038d00000UbgxRAAR')
    # res = salesforce_req(credentials.access_token, '')
    logger.info(res)
    return HttpResponse(json.dumps(res, indent=4), content_type="application/json")
