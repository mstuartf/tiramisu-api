
master = """\n
"{full_name}'s LinkedIn headline is:
{headline}.
   
Their summary is:
{summary}

Write 5 ice breakers (in English) to start a conversation with {full_name} that make a reference to information on their profile.

The ice breakers should be in the following style:
{style}\

They should be numbered from 1 to 5.
"""


def build_prompt(prompt, prospect):
    return master.format(
        full_name=prospect.full_name,
        headline=prospect.headline,
        summary=prospect.summary,
        style=prompt.text
    )
