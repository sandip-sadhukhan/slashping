from django.urls import path
from accounts import views

urlpatterns = [
    path('logout/', views.logout, name='logout'),
]