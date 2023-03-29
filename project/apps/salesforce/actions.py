import json
import logging

from django.http import HttpResponse

from .auth import salesforce_req

logger = logging.getLogger(__name__)


def lookup_contact_id(credentials, slug):
    field_name = '{}{}'.format(
        credentials.linkedin_field_name,
        "__c" if credentials.linkedin_field_is_custom else "",
    )

    res = salesforce_req(credentials, 'get', 'query', params={
        'q': r"SELECT Id, {} FROM Contact WHERE {} LIKE '%{}%'".format(
            field_name,
            field_name,
            slug,
        )
    })
    logger.info(res)
    if res['totalSize'] > 1:
        raise Exception('too many contacts matching {}'.format(slug))
    if res['totalSize'] < 1:
        raise Exception('no contacts matching {}'.format(slug))
    return res['records'][0]['Id']


def create_linkedin_msg_task(credentials, contact_id, description):
    # todo: "OwnerId": user_id,
    res = salesforce_req(credentials, 'post', 'sobjects/Task', json={
        "WhoId": contact_id,
        "Subject": "LinkedIn message",
        "Status": "Completed",
        "Description": description,
    })
    logger.info(res)
    return res
