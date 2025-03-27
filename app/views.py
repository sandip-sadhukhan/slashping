import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from app.constants import CustomerTabs
from app import forms

def home(request):
    return render(request, 'home.html')

# Intermediate route for going to dashboard
@login_required
def dashboard(request):
    return redirect(f"{reverse("customers")}?tab={CustomerTabs.PENDING_TODAY.value}")

@login_required
def customers(request):
    tab = request.GET.get("tab")

    try:
        tab = CustomerTabs(tab)
    except ValueError:
        return redirect("dashboard")
    
    context = {
        'tab': tab,
        'CustomerTabs': CustomerTabs
    }

    return render(request, 'dashboard/customers.html', context)

@login_required
def reminder(request):
    context = {}

    if request.method == "POST":
        form = forms.ReminderSettings(data=request.POST)

        if form.is_valid():
            request.user.new_client_target = form.cleaned_data.get("new_client_target")
            request.user.new_client_in_days = form.cleaned_data.get("new_client_in_days")
            request.user.save()
            messages.add_message(request, messages.SUCCESS, "Settings saved successfully")

            return redirect("reminder")
        else:
            context["form"] = form

    return render(request, 'dashboard/reminder.html', context)

@login_required
@require_POST
def save_customer_mail_time(request):
    form = forms.CustomerMailTimeForm(request.POST)

    if not form.is_valid():
        import ipdb
        ipdb.set_trace()

    hour = form.cleaned_data.get("hour")
    minute = form.cleaned_data.get("minute")
    user = request.user
    user.reminder_email_time = datetime.time(hour=hour, minute=minute)
    user.save()

    return render(request, "partials/toastr.html",
                  {"message": "Time saved successfully", "type": "success"})