# Generated by Django 3.2 on 2023-03-24 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prompts', '0003_prompt_deprecated'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Prompt',
        ),
    ]
