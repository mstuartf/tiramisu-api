import logging
import os

import requests

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
        logger.info(res.content)
        raise

    return res.json()


def refresh(refresh_token):
    res = requests.post(
        "https://login.salesforce.com/services/oauth2/token",
        params={
          'refresh_token': "{}".format(refresh_token),
          'grant_type': 'refresh_token',
          'client_id': os.environ['SALESFORCE_CONSUMER_KEY'],
          'client_secret': os.environ['SALESFORCE_CONSUMER_SECRET'],
        },
    )
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        logger.info(res.content)
        raise

    return res.json()


def salesforce_req(credentials, method, path, auto_refresh=True, **kwargs):
    res = requests.request(
        method,
        "{}/services/data/v57.0/{}".format(credentials.instance_url, path),
        headers={
          'Authorization': "Bearer {}".format(credentials.access_token),
          'Content-Type': 'application/json',
        },
        **kwargs,
    )
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        if res.status_code == 401 and auto_refresh:
            logger.info('token has expired; refreshing and retrying')
            tokens = refresh(credentials.refresh_token)
            credentials.access_token = tokens['access_token']
            credentials.issued_at = tokens['issued_at']
            credentials.save()
            return salesforce_req(credentials, method, path, auto_refresh=False, **kwargs)
        logger.info(res.content)
        raise

    return res.json()