skeleton = """\n
Draft 3 messages to {full_name}
Their LinkedIn headline is: {headline}
Their summary is: {summary}

The messages should:
* Start 'Hi [first name]', and end 'Kind regards'
* Have a {style} style 

{sections}"""


def build_chat_messages(template, prospect):
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant that drafts LinkedIn messages for salespeople."
        },
        {
            "role": "system",
            "content": "You only speak JSON. Do not print normal text. Print an array only. For each message, add an object to the array with the key 'message'."
        },
        {
            "role": "system",
            "content": "Do not use any placeholder variables."
        },
        {
            "role": "user",
            "content": skeleton.format(
                full_name=prospect.full_name,
                headline=prospect.headline,
                summary=prospect.summary or "",
                style=template.parse_style(),
                sections=template.parse_sections(),
            )
        }
    ]
