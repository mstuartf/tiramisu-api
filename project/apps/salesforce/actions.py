import logging

from .auth import salesforce_req

logger = logging.getLogger(__name__)


def lookup_contact_id(credentials, slug):
    field_name = credentials.linkedin_field_name

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


def lookup_user_id(credentials, email_address):
    res = salesforce_req(credentials, 'get', 'query', params={
        'q': r"SELECT Id, FirstName, LastName FROM User WHERE Email LIKE '{}'".format(
            email_address,
        )
    })
    logger.info(res)
    if res['totalSize'] > 1:
        raise Exception('too many users matching {}'.format(email_address))
    if res['totalSize'] < 1:
        raise Exception('no users matching {}'.format(email_address))
    return res['records'][0]['Id']


def create_linkedin_msg_task(credentials, contact_id, user_id, description):
    res = salesforce_req(credentials, 'post', 'sobjects/Task', json={
        "WhoId": contact_id,
        "OwnerId": user_id,
        # "CreatedById": user_id, <-- INVALID_FIELD_FOR_INSERT_UPDATE
        "Subject": "LinkedIn message",
        "Status": "Completed",
        "Description": description,
    })
    logger.info(res)
    return res
