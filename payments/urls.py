from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path('initiate/<str:order_ids>/', views.initiate_payment, name='initiate_payment'),
    path("callback/", views.phonepe_callback, name="phonepe_callback"),
]

