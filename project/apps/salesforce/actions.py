import json
import logging

from django.http import HttpResponse

from .auth import salesforce_req

logger = logging.getLogger(__name__)


# {
#     "totalSize": 1,
#     "done": true,
#     "records": [
#         {
#             "attributes": {
#                 "type": "Contact",
#                 "url": "/services/data/v57.0/sobjects/Contact/0038d00000UbgxQAAR"
#             },
#             "Id": "0038d00000UbgxQAAR",
#             "Name": "Andy Young",
#             "LinkedIn_Url__c": "https://www.linkedin.com/in/mstuartf/"
#         }
#     ]
# }
def lookup_contact_id(credentials, linkedin_field_name, slug):
    res = salesforce_req(credentials, 'get', 'query', params={
        'q': r"SELECT Id, {}__c FROM Contact WHERE {}__c LIKE '%{}%'".format(
            linkedin_field_name,
            linkedin_field_name,
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
    return HttpResponse('ok', content_type="application/json")
