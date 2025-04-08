from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import (
    logout as auth_logout,
    login as auth_login,
    authenticate,
)
from django.views.decorators.http import require_http_methods
from lib.decorators import anonymous_required
from accounts.forms import LoginForm, SignupForm,  GoogleLoginCallbackForm
from accounts.models import User
from django.contrib import messages
from lib.google_auth import GoogleRawLoginFlowService
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from django.core.files import File
from app.tasks import send_google_signup_mail


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


@anonymous_required
@require_http_methods(['GET'])
def google_login(request):
    google_login_flow = GoogleRawLoginFlowService()

    authorization_url, state = google_login_flow.get_authorization_url()

    request.session['google_oauth2_state'] = state

    return redirect(authorization_url)

@anonymous_required
@require_http_methods(['GET'])
def google_callback(request):
    # Validation Part
    form = GoogleLoginCallbackForm(request.GET)
    form.is_valid()

    validated_data = form.cleaned_data

    code = validated_data.get('code')
    state = validated_data.get('state')
    error = validated_data.get('error')

    if error:
        messages.add_message(request, messages.ERROR, error)
        return redirect('login')
    
    if not code or not state:
        messages.add_message(request, messages.ERROR, "Code & state are required")
        return redirect('login')
    
    session_state = request.session.get("google_oauth2_state")

    if session_state is None:
        messages.add_message(request, messages.ERROR, "CSRF check failed!")
        return redirect('login')

    del request.session["google_oauth2_state"]

    if state != session_state:
        messages.add_message(request, messages.ERROR, "CSRF check failed!")
        return redirect('login')
    
    # Get user data
    google_login_flow = GoogleRawLoginFlowService()
    google_tokens = google_login_flow.get_tokens(code=code)
    id_token_decoded = google_tokens.decode_id_token()

    if not id_token_decoded or not id_token_decoded.get('email') or not id_token_decoded.get('name'):
        messages.add_message(request, messages.ERROR, "Invalid ID token")
        return redirect('login')

    email = id_token_decoded.get('email')
    name = id_token_decoded.get('name')
    picture = id_token_decoded.get('picture')

    user = User.objects.filter(email=email).first()

    # Sign up user if not exists
    if user is None:
        user = User.objects.create_user(email=email, name=name)
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()

        if picture:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(picture).read())
            img_temp.flush()

            user.profile_image.save(f"{picture.split("/")[-1]}.jpg", File(img_temp))

        auth_login(request, user)
        messages.add_message(request, messages.SUCCESS, 'You have successfully signed up with Google')

        # Send mail to user with password, call the celery task
        send_google_signup_mail.delay(user.id, password)

    # Login user if exists
    else:
        auth_login(request, user)
        messages.add_message(request, messages.SUCCESS, 'You have successfully logged in with Google')
    
    return redirect('dashboard')

