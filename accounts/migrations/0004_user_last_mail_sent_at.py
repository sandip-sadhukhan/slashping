# Generated by Django 5.1.4 on 2025-03-31 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_user_profile_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="last_mail_sent_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
