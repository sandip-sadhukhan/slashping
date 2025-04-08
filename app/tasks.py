from django.utils import timezone
from django.db.models import F, Q, ExpressionWrapper, DateTimeField
from django.db.models.functions import ExtractHour, ExtractMinute, TruncDate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from celery import shared_task

from accounts.models import User
from .models import Client


@shared_task
def send_customers_mail():
    now = timezone.now()

    users = User.objects.annotate(
        next_mail_should_sent_at=ExpressionWrapper(
            TruncDate('last_customers_mail_sent_at') +
            timezone.timedelta(days=1) +
            (ExtractHour('reminder_email_time') * 60 + ExtractMinute('reminder_email_time')) * timezone.timedelta(minutes=1),
            output_field=DateTimeField()
        )
    ).filter(
        Q(last_customers_mail_sent_at__isnull=True) |
        Q(next_mail_should_sent_at__lte=now)
    )

    for user in users:
        clients = Client.objects.pending_todays_clients().filter(created_by=user)

        context = {
            'user': user,
            'clients': clients,
            'SITE_URL': settings.SITE_URL
        }

        html_message = render_to_string('emails/customers_mail.html', context)

        if clients.count() > 0:
            send_mail(
                "Customers Mail from SlashPing",
                "This is a customers mail from SlashPing",
                None,
                [user.email],
                html_message=html_message
            )
        
        user.last_customer_mail_sent_at = now
        user.save()

    return True

@shared_task
def send_reminder_mail():
    users = User.objects\
        .filter(
            last_reminder_calculation_done_at__isnull=False,
            last_reminder_calculation_done_at__lte=ExpressionWrapper(
                timezone.now() - F('new_client_in_days') * timezone.timedelta(days=1),
                output_field=DateTimeField()
            )
        )

    for user in users:
        user.pending_clients += user.new_client_target
        user.last_reminder_calculation_done_at = timezone.now()
        user.save()

        context = {
            'user': user,
            'SITE_URL': settings.SITE_URL
        }

        html_message = render_to_string('emails/reminder_mail.html', context)

        if user.new_client_target > 0:
            send_mail(
                "Reminder Mail from SlashPing",
                "This is a reminder mail from SlashPing",
                None,
                [user.email],
                html_message=html_message
            )
        
    return True

@shared_task
def send_google_signup_mail(user_id, password):
    user = User.objects.get(id=user_id)

    context = {
        'user': user,
        'password': password,
        'SITE_URL': settings.SITE_URL
    }

    html_message = render_to_string('emails/google_signup_mail.html', context)

    send_mail(
        "Google Signup Mail from SlashPing",
        "This is a Google signup mail from SlashPing",
        None,
        [user.email],
        html_message=html_message
    )

    return True
