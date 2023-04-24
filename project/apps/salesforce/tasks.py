import logging
from celery import shared_task

from .actions import lookup_contact_id, create_salesforce_task, lookup_user_id
from .models import Credentials, Task
from ..messages.models import LinkedInMessage, LinkedInLike, LinkedInComment

logger = logging.getLogger(__name__)


@shared_task()
def create_salesforce_msg_task(pk):
    logger.info("uploading linkedin message {} to salesforce".format(pk))
    msg = LinkedInMessage.objects.get(pk=pk)
    try:
        logger.info("looking for {}'s credentials".format(msg.user.company.name))
        credentials = Credentials.objects.get(company=msg.user.company)

        if credentials.linkedin_field_name is None:
            raise Exception('linked in field name has not been configured')

        contact_id = lookup_contact_id(credentials, msg.profile_slug)
        user_id = lookup_user_id(credentials, msg.user.email)
        res = create_salesforce_task("LinkedIn: message", credentials, contact_id, user_id, msg.content)

        if not res['success']:
            logger.info(res['errors'])
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


@shared_task()
def create_salesforce_like_task(pk):
    logger.info("uploading linkedin like {} to salesforce".format(pk))
    like = LinkedInLike.objects.get(pk=pk)
    try:
        logger.info("looking for {}'s credentials".format(like.user.company.name))
        credentials = Credentials.objects.get(company=like.user.company)

        if credentials.linkedin_field_name is None:
            raise Exception('linked in field name has not been configured')

        contact_id = lookup_contact_id(credentials, like.profile_slug)
        user_id = lookup_user_id(credentials, like.user.email)
        res = create_salesforce_task("LinkedIn: liked post", credentials, contact_id, user_id, like.post_content)

        if not res['success']:
            logger.info(res['errors'])
            raise Exception("|".join(res['errors']))

        Task.objects.create(like=like, task_id=res["id"])
        like.processed = True
        like.save()

    except Exception as e:
        logger.info(e)
        like.processed = True
        like.error = "{}".format(e)
        like.save()
    return True



@shared_task()
def create_salesforce_comment_task(pk):
    logger.info("uploading linkedin comment {} to salesforce".format(pk))
    comment = LinkedInComment.objects.get(pk=pk)
    try:
        logger.info("looking for {}'s credentials".format(comment.user.company.name))
        credentials = Credentials.objects.get(company=comment.user.company)

        if credentials.linkedin_field_name is None:
            raise Exception('linked in field name has not been configured')

        contact_id = lookup_contact_id(credentials, comment.profile_slug)
        user_id = lookup_user_id(credentials, comment.user.email)
        res = create_salesforce_task("LinkedIn: post comment", credentials, contact_id, user_id, comment.post_content)

        if not res['success']:
            logger.info(res['errors'])
            raise Exception("|".join(res['errors']))

        Task.objects.create(comment=comment, task_id=res["id"])
        comment.processed = True
        comment.save()

    except Exception as e:
        logger.info(e)
        comment.processed = True
        comment.error = "{}".format(e)
        comment.save()
    return True
