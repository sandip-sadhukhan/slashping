import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Define periodic tasks
app.conf.beat_schedule = {
    'sending-reminder-mail-every-30-minutes': {
        'task': 'app.tasks.send_customers_mail',
        'schedule': crontab(minute='*/1'),  # Every 30 minutes
    },
}
