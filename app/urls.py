from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customers/', views.customers, name='customers'),
    path('reminder/', views.reminder, name='reminder'),
    # path('save_customer_mail_time/', views.save_customer_mail_time, name='save_customer_mail_time'),
]