from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from app.constants import CustomerTabs

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