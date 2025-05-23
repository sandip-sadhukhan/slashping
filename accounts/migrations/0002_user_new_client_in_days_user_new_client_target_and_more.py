# Generated by Django 5.1.4 on 2025-03-26 08:07

import accounts.models
import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="new_client_in_days",
            field=models.PositiveIntegerField(
                default=7,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(30),
                ],
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="new_client_target",
            field=models.PositiveIntegerField(
                default=0, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="profile_image",
            field=models.ImageField(
                null=True, upload_to=accounts.models.user_directory_path
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="reminder_email_time",
            field=models.TimeField(default=datetime.time(8, 0)),
        ),
    ]
