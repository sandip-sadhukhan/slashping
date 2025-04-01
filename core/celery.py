import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Define periodic tasks
app.conf.beat_schedule = {
    'sending-customer-mail-every-30-minutes': {
        'task': 'app.tasks.send_customers_mail',
        'schedule': crontab(minute='*/30', hour='0-23'),  # Every 30 minutes starting from 00:00
    },
    'sending-reminder-mail-every-day': {
        'task': 'app.tasks.send_reminder_mail',
        'schedule': crontab(minute=0, hour=8),  # Every day
    },
}
