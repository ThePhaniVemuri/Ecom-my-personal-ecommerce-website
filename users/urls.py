"""URL patterns for the users app"""
from django.urls import path,include
from . import views

app_name='users'
urlpatterns=[
    path('',include('django.contrib.auth.urls')),
    path('register/',views.register,name='register'),
    path('logoutt/',views.logoutt,name='logoutt'),    
    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    # Add a URL for the checkout functionality (explained below)
    path('checkout/', views.checkout, name='checkout')
    ]
