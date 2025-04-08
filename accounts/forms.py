from django import forms
from accounts.models import User

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']

class GoogleLoginCallbackForm(forms.Form):
    code = forms.CharField(required=False)
    state = forms.CharField(required=False)
    error = forms.CharField(required=False)