# Generated by Django 3.2 on 2023-03-31 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salesforce', '0004_auto_20230329_2037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credentials',
            name='linkedin_field_is_custom',
        ),
    ]
