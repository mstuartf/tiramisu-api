# Generated by Django 3.2 on 2023-03-14 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prospects', '0004_auto_20230314_2105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prospect',
            name='raw',
        ),
        migrations.AddField(
            model_name='prospect',
            name='talks_about',
            field=models.TextField(blank=True, null=True),
        ),
    ]
