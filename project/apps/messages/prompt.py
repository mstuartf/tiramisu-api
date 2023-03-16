
master = """\n
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
    return master.format(
        full_name=prospect.full_name,
        headline=prospect.headline,
        summary=prospect.summary,
        rules=prompt.text
    )
