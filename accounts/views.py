from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import (
    logout as auth_logout,
    login as auth_login,
    authenticate,
)
from django.views.decorators.http import require_http_methods
from lib.decorators import anonymous_required
from accounts.forms import LoginForm, SignupForm
from django.contrib import messages

@anonymous_required
@require_http_methods(['GET', 'POST'])
def login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                auth_login(request, user)

                messages.add_message(request, messages.SUCCESS, 'You have successfully logged in')

                response = HttpResponse()
                response['HX-Redirect'] = reverse('dashboard')
                return response
            else:
                form.errors['email'] = ["Invalid email or password"]

        return render(request, 'accounts/login.html#login-form', {'login_form': form})

    return render(request, 'accounts/login.html', {'login_form': form})

@anonymous_required
@require_http_methods(['GET', 'POST'])
def signup(request):
    form = SignupForm()

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()

            messages.add_message(request, messages.SUCCESS, 'You have successfully signed up')

            user = authenticate(email=user.email, password=form.cleaned_data.get('password'))
            auth_login(request, user)

            response = HttpResponse()
            response['HX-Redirect'] = reverse('dashboard')
            return response

        return render(request, 'accounts/signup.html#signup-form', {'signup_form': form})

    
    return render(request, 'accounts/signup.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

