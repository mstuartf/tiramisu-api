import json
import logging
from celery import shared_task
from openai.error import RateLimitError, ServiceUnavailableError

from .chat import draft_chat_messages
from .models import MessageSet
from .prompt import build_chat_messages
from .serializers import WriteMessageSetSerializer

logger = logging.getLogger(__name__)


@shared_task()
def generate_message_task(pk):
    logger.info("generating messages for set {}".format(pk))
    ms = MessageSet.objects.get(pk=pk)
    try:
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
    except Exception as e:
        ms.processed = True
        ms.error = "{}".format(e)
        ms.save()
    return True
