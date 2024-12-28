"""URLs are defined for the sellers app"""
from django.urls import path,include

from . import views
from .views import SellerLoginView

app_name='sellers'
urlpatterns=[
    path('login/', SellerLoginView.as_view(), name='seller_login'),
    path('register/', views.register_seller, name='register_seller'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_product/', views.add_product, name='add_product'),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
    ]
