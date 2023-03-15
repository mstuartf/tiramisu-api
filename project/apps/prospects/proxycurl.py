# todo: REMOVE_V1

import os
import logging
import requests

logger = logging.getLogger(__name__)

TOKEN = os.environ.get("PROXYCURL_TOKEN")
BASE_URL = "https://nubela.co"


def fetch_profile_request(slug):
    res = requests.get(
        "{}/proxycurl/api/v2/linkedin".format(
            BASE_URL
        ),
        params={
            'url': "https://www.linkedin.com/in/{}".format(slug),
            'use_cache': 'if-recent',
        },
        headers={
            'Authorization': 'Bearer {}'.format(TOKEN)
        }
    )
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        logger.info(res.json())
        raise

    return res.json()
