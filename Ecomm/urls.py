"""Defines url patterns for the app (not the project)"""

from django.urls import path

from . import views

app_name='Ecomm'
urlpatterns=[
    #Home page
    path('',views.Category_list,name='Home_page'),
    #For new category
    path('add_category/',views.add_category,name='add_category'),
    path('add_sub_category/',views.add_sub_category,name='add_sub_category'),
    path('Sub_category_list/<str:category_name>/',views.Sub_category_list,name='Sub_category_list')
]
