# Generated by Django 3.2 on 2023-04-19 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_openai_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='msg_tracking_enabled',
            new_name='linkedin_tracking_enabled',
        ),
        migrations.AddField(
            model_name='customuser',
            name='comment_tracking_activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='like_tracking_activated',
            field=models.BooleanField(default=False),
        ),
    ]
