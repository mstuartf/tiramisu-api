import os
import openai
import logging

logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


def draft_chat_messages(messages, temperature=0.7, model="gpt-3.5-turbo"):
    logger.info("using model {}".format(model))
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=512
    )
    logger.info(response)
    return response
