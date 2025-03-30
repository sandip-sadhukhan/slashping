from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator 
from app import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomerMailTimeForm(forms.Form):
    hour = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    minute = forms.IntegerField()

    def clean_minute(self):
        minute = self.cleaned_data.get("minute")

        if minute and minute not in [0, 30]:
            self.add_error("minute", "Minutes must be either 0 or 30")

        return minute


class ReminderSettings(forms.Form):
    new_client_target = forms.IntegerField(validators=[MinValueValidator(0)])
    new_client_in_days = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])


class ClientForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = ['name', 'contact_link', 'note', 'remind_me_in_days']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'profile_image']