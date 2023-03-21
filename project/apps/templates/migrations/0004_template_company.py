# Generated by Django 3.2 on 2023-03-21 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        ('templates', '0003_auto_20230319_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.company'),
        ),
    ]
