import logging
from celery import shared_task

from .actions import lookup_contact_id, create_linkedin_msg_task
from .models import Credentials, Task
from ..messages.models import LinkedInMessage

logger = logging.getLogger(__name__)


@shared_task()
def create_salesforce_task(pk):
    logger.info("uploading linkedin message {} to salesforce".format(pk))
    msg = LinkedInMessage.objects.get(pk=pk)
    try:
        logger.info("looking for {}'s credentials".format(msg.user.company.name))
        credentials = Credentials.objects.get(company=msg.user.company)
        contact_id = lookup_contact_id(credentials, 'LinkedIn_Url', msg.profile_slug)
        res = create_linkedin_msg_task(credentials, contact_id, msg.content)
        logger.info(res)
        if not res['success']:
            raise Exception("|".join(res['errors']))
        Task.objects.create(msg=msg, task_id=res["id"])
        msg.processed = True
        msg.save()
    except Exception as e:
        logger.info(e)
        msg.processed = True
        msg.error = "{}".format(e)
        msg.save()
    return True
