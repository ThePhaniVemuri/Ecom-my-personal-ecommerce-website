"""
URL configuration for Ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface
    path('', include('Ecomm.urls')),  # Include the general app (Ecomm)
    path('products/', include('products.urls')),  # Include the products app
    path('users/', include('users.urls')),  # Include the users app (if you have one)
    path('sellers/', include('sellers.urls')),
    path('orders/', include('orders.urls')),
    path("payments/", include("payments.urls")),

]
