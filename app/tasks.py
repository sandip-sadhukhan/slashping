from celery import shared_task
from django.utils import timezone
from .models import Client
from accounts.models import User


# Send mail at 8:30 AM
@shared_task
def send_customers_mail():
    print("Send Customers mail")
    users = User.objects.all()

    for user in users:
        print(user.email)

    return True