from django.urls import path,include
from . import views

app_name='orders'
urlpatterns=[
    path('order_history/', views.order_history, name='order_history'),
    path('place_order/<int:product_id>/', views.place_order, name='place_order'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    ]
