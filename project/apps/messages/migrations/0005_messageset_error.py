# Generated by Django 3.2 on 2023-03-23 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openai_messages', '0004_auto_20230320_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='messageset',
            name='error',
            field=models.TextField(blank=True, null=True),
        ),
    ]