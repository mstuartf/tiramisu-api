v1 = """\n
"{full_name}'s LinkedIn headline is:
{headline}.
   
Their summary is:
{summary}

Write 5 messages (numbered 1-5) that I could send to start a conversation with {full_name} that make a reference to \
information on their profile.

The messages should follow these rules:
* No line breaks
{rules}\
"""


def build_prompt(prompt, prospect):
    return v1.format(
        full_name=prospect.full_name,
        headline=prospect.headline,
        summary=prospect.summary,
        rules=prompt.text
    )


v3 = """\n
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
            "role": "user",
            "content": v3.format(
                full_name=prospect.full_name,
                headline=prospect.headline,
                summary=prospect.summary or "",
                style=template.parse_style(),
                sections=template.parse_sections(),
            )
        }
    ]
