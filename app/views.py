import datetime
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import (
    require_POST, require_http_methods
)
from django.contrib import messages

from app.constants import CustomerTabs
from app import forms, models

def home(request):
    return render(request, 'home.html')

# Intermediate route for going to dashboard
@login_required
def dashboard(request):
    params = request.GET.copy()
    try:
        tab = CustomerTabs(params.get('tab')).value
    except ValueError:
        tab = CustomerTabs.PENDING_TODAY.value

    params['tab'] = tab

    return redirect(f"{reverse('customers')}?{params.urlencode()}")

@login_required
def customers(request):
    tab = request.GET.get("tab")

    try:
        tab = CustomerTabs(tab)
    except ValueError:
        return redirect("dashboard")
    
    reminder_email_time_form = forms.CustomerMailTimeForm(
        data={"hour": request.user.reminder_email_time.hour,
              "minute": request.user.reminder_email_time.minute})
    
    clients = models.Client.objects\
        .filter(created_by=request.user)
    
    tabCounts = {
        CustomerTabs.PENDING_TODAY.value: clients.pending_todays_clients().count(),
        CustomerTabs.PENDING_TOMORROW.value: clients.pending_tomorrows_clients().count(),
        CustomerTabs.ALL_CLIENTS.value: clients.count()
    }
    
    if tab == CustomerTabs.PENDING_TODAY:
        clients = clients.pending_todays_clients()
    elif tab == CustomerTabs.PENDING_TOMORROW:
        clients = clients.pending_tomorrows_clients()
    
    if tab in [CustomerTabs.PENDING_TODAY, CustomerTabs.PENDING_TOMORROW]:
        clients = clients.order_by('reminder_date')
    else:
        clients = clients.order_by('created_at')
    
    context = {
        'tab': tab,
        'CustomerTabs': CustomerTabs,
        'reminder_email_time_form': reminder_email_time_form,
        'create_client_form': forms.ClientForm(),
        'clients': clients,
        'tabCounts': tabCounts,
        'today': datetime.date.today(),
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
        response = render(request, 'dashboard/customers.html#reminder-settings-form', {"reminder_email_time_form": form})
        response['HX-Retarget'] = '#reminder_settings_form'
        response['HX-Reswap'] = 'outerHTML'
        response['DATA-Form-Error'] = 'true'

        return response

    hour = form.cleaned_data.get("hour")
    minute = form.cleaned_data.get("minute")
    user = request.user
    user.reminder_email_time = datetime.time(hour=hour, minute=minute)
    user.save()

    return render(request, "partials/toastr.html",
                  {"message": "Time saved successfully", "type": "success"})

@login_required
@require_POST
def create_client(request):
    form = forms.ClientForm(data=request.POST)

    if not form.is_valid():
        response = render(request, 'dashboard/customers.html#new-client-form', {"create_client_form": form})
        return response
    
    models.Client.objects.create(
        name=form.cleaned_data.get("name"),
        contact_link=form.cleaned_data.get("contact_link"),
        note=form.cleaned_data.get("note"),
        remind_me_in_days=form.cleaned_data.get("remind_me_in_days"),
        created_by=request.user
    )

    add_another_client = request.POST.get('add_another_client', False)

    messages.add_message(request, messages.SUCCESS, "Client created successfully")
    response = HttpResponse()

    if add_another_client:
        response['HX-Redirect'] = request.headers['Hx-Current-url'] + "&open_new_client_modal=true"
    else:
        response['HX-Refresh'] = 'true'

    return response

@login_required
@require_http_methods(["POST", "GET"])
def ping_client(request, client_id):
    from_email = request.GET.get("origin") == "EMAIL"

    # Get request only available for email users
    if request.method == 'GET' and not from_email:
        return redirect("dashboard")

    client = get_object_or_404(models.Client, id=client_id, created_by=request.user)
    client.ping()

    messages.add_message(request, messages.SUCCESS, "Client pinged successfully")

    if from_email:
        return redirect('dashboard')

    response = HttpResponse()
    response['HX-Refresh'] = 'true'
    return response

@login_required
@require_http_methods(['DELETE'])
def delete_client(request, client_id):
    client = get_object_or_404(models.Client, id=client_id, created_by=request.user)
    client.delete()

    response = HttpResponse()
    response['HX-Refresh'] = 'true'
    return response

@login_required
@require_http_methods(['GET', 'POST'])
def edit_client(request, client_id):
    client = get_object_or_404(models.Client, id=client_id, created_by=request.user)
    form = forms.ClientForm(instance=client)

    if request.method == 'POST':
        form = forms.ClientForm(data=request.POST)

        if not form.is_valid():
            return render(request, 'dashboard/customers.html#edit-client-form',
                {"client": client, 'edit_client_form': form})
            
        client.name = form.cleaned_data.get("name")
        client.contact_link = form.cleaned_data.get("contact_link")
        client.note = form.cleaned_data.get("note")
        client.remind_me_in_days = form.cleaned_data.get("remind_me_in_days")
        client.save()

        messages.add_message(request, messages.SUCCESS, "Client updated successfully")

        response = HttpResponse()
        response['HX-Refresh'] = 'true'
        return response

    return render(request, 'dashboard/customers.html#edit-client-form',
                  {"client": client, 'edit_client_form': form})

@login_required
def profile_page(request):
    if request.method == 'POST':
        form = forms.ProfileForm(data=request.POST, files=request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Profile updated successfully")

            return redirect('profile_page')
        else:
            messages.add_message(request, messages.ERROR, "Profile update failed")
    else:
        form = forms.ProfileForm(instance=request.user)


    return render(request, 'dashboard/profile_page.html', {'profile_form': form})

@login_required
@require_http_methods(['GET', 'POST'])
def reset_pending_counts(request):
    from_email = request.GET.get("origin") == "EMAIL"

    # Get request only available for email users
    if request.method == 'GET' and not from_email:
        return redirect("dashboard")

    user = request.user
    user.pending_clients = 0
    user.save()

    messages.add_message(request, messages.SUCCESS, "Counts reset successfully")

    if from_email:
        return redirect('reminder')

    response = HttpResponse()

    response['HX-Refresh'] = 'true'

    return response
