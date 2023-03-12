
master = """\n
"{first_name}'s LinkedIn headline is:
{headline}.
   
Their summary is:
{summary}

Write up to 5 ice breakers (in English) to start a conversation with {first_name} that make a reference to information on their profile.

The ice breakers should be in the following style:
{style}\
"""


def build_prompt(prompt, prospect):
    return master.format(
        first_name=prospect.first_name,
        headline=prospect.headline,
        summary=prospect.summary,
        style=prompt.text
    )
