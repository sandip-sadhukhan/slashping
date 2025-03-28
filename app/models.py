from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class Client(models.Model):
    name = models.CharField(max_length=200)
    contact_link = models.URLField(max_length=500)
    note = models.TextField(blank=True)
    remind_me_in_days = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='clients', on_delete=models.CASCADE)

    last_pinged_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name