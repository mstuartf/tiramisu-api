import os
import openai
import logging

logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


def draft_messages(prompt, temperature=0.7):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=temperature,
        max_tokens=512
    )
    logger.info(response)
    return response
