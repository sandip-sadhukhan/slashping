from django.shortcuts import render, redirect
from django.contrib.auth import (
    logout as auth_logout,
    login as auth_login,
    authenticate,
)
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET', 'POST'])
def login(request):
    return render(request, 'accounts/login.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

