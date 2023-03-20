import json
import logging
from celery import shared_task
from openai.error import RateLimitError, ServiceUnavailableError

from .chat import draft_chat_messages
from .models import MessageSet
from .prompt import build_chat_messages
from .serializers import WriteMessageSetSerializer

OPENAI_ERRORS = (
    RateLimitError,
    ServiceUnavailableError,
)

logger = logging.getLogger(__name__)


@shared_task(autoretry_for=OPENAI_ERRORS)
def generate_message_task(pk):
    logger.info("generating messages for set {}".format(pk))
    ms = MessageSet.objects.get(pk=pk)
    logger.info("drafting messages")
    chat_messages = build_chat_messages(ms.template, ms.prospect)
    logger.info("calling openai api")
    raw = draft_chat_messages(chat_messages)
    logger.info(raw)
    raw_messages = raw["choices"][0]["message"]["content"].replace("`", "")

    start = raw_messages.find('[')
    end = raw_messages.find(']')
    logger.info(raw_messages[start:end + 1])

    messages = [{"parsed": m["message"]} for m in json.loads(raw_messages[start:end + 1])]
    logger.info(messages)

    data = {
        "processed": True,
        "raw": raw,
        "messages": messages
    }

    serializer = WriteMessageSetSerializer(ms, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    logger.info("success")
    return True
