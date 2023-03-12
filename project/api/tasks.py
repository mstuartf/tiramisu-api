import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def deferred_task():
    logger.info("deferred_task triggered")
    return True
