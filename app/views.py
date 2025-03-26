from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

# Intermediate route for going to dashboard
@login_required
def dashboard(request):
    return redirect("customers")

@login_required
def customers(request):
    return render(request, 'dashboard/customers.html')