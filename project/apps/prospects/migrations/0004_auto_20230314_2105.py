# Generated by Django 3.2 on 2023-03-14 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prospects', '0003_alter_prospect_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prospect',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='prospect',
            name='last_name',
        ),
    ]
