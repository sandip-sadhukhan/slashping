from django.db import models
from django.db.models import DateTimeField, ExpressionWrapper, F, Q
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class ClientQuerySet(models.QuerySet):
    def _annotate_reminder_date(self):
        return self.annotate(
            reminder_date=ExpressionWrapper(
                F('last_pinged_at') + F('remind_me_in_days') * timezone.timedelta(days=1),
                output_field=DateTimeField()
            )
        )

    def pending_todays_clients(self):
        today = timezone.now().date()

        return self._annotate_reminder_date()\
            .filter(Q(last_pinged_at__isnull=True) |
                    Q(reminder_date__date__lte=today))

    def pending_tomorrows_clients(self):
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)

        return self._annotate_reminder_date()\
            .filter(reminder_date__date__lte=tomorrow)


class Client(models.Model):
    name = models.CharField(max_length=200)
    contact_link = models.URLField(max_length=500)
    note = models.TextField(blank=True)
    remind_me_in_days = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='clients', on_delete=models.CASCADE)

    last_pinged_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ClientQuerySet.as_manager()

    def __str__(self):
        return self.name
    
    def ping(self):
        self.last_pinged_at = timezone.now()
        self.save()