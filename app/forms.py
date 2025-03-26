from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

class CustomerMailTimeForm(forms.Form):
    hour = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    minute = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(59)])
    

class ReminderSettings(forms.Form):
    new_client_target = forms.IntegerField(validators=[MinValueValidator(0)])
    new_client_in_days = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])