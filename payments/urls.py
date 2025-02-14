from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path('initiate/', views.viewPage, name='viewPage'),
    path("callback/", views.phonepe_callback, name="phonepe_callback"),
]

