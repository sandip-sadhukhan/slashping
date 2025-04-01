from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customers/', views.customers, name='customers'),
    path('reminder/', views.reminder, name='reminder'),
    path('save_customer_mail_time/', views.save_customer_mail_time, name='save_customer_mail_time'),
    path('create_client/', views.create_client, name='create_client'),
    path('ping_client/<int:client_id>/', views.ping_client, name='ping_client'),
    path('delete_client/<int:client_id>/', views.delete_client, name='delete_client'),
    path('edit_client/<int:client_id>/', views.edit_client, name='edit_client'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('reset_pending_counts/', views.reset_pending_counts, name='reset_pending_counts'),
]