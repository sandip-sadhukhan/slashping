from django import forms
from accounts.models import User

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
