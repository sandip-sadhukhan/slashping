from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

class CustomerMailTimeForm(forms.Form):
    hour = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    minute = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(59)])
    