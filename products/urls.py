"""URLs are defined for the products app"""
from django.urls import path

from . import views

app_name='products'
urlpatterns=[
    #subcategory url
    path('Products_in_sub_category/<str:sub_category_name>/', views.Products_in_sub_category, name='Products_in_sub_category'),
    #search page
    path('search_results/',views.search_bar,name='search_bar')
    ]
