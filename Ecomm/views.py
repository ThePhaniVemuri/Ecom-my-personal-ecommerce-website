from django.shortcuts import render, redirect, get_object_or_404

from .models import Category, Sub_category
from .forms import CategoryForm, Sub_categoryForm
from users.models import Cart

from django.contrib.auth.decorators import user_passes_test

def superuser_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view_func

def is_seller(user):
    return hasattr(user, 'seller')

def Category_list(request):
    """Lists all the Categories of products"""
    Categories=Category.objects.all()
    Sub_categories = Sub_category.objects.all()
    cart_items=Cart.objects.all()
    context={'Categories':Categories,'Sub_categories': Sub_categories,'cart_items':cart_items,'is_seller':is_seller}
    
    return render(request,'Ecomm/base.html',context)

def add_category(request):
    """Adding new category(acctually this is for seller)"""
    if request.method!='POST':
        #create a blank form
        form=CategoryForm()
    else:
        #post method , data is submitted
        form=CategoryForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('Ecomm:Home_page')

    context={'form':form}
    return render(request,'Ecomm/add_category.html',context)

def Sub_category_list(request, category_name):
    """Lists all subcategories for a given category."""
    Sub_categories = Sub_category.objects.filter(category_of_subcategory__category_name__iexact=category_name.strip())
    Categories = Category.objects.all()
    context = {
        'Sub_categories': Sub_categories,
        'Categories': Categories,
    }
    return render(request, 'Ecomm/base.html', context)

def add_sub_category(request):
    """Adding new sub-category(acctually this is for seller)"""
    if request.method!='POST':
        #create a blank form
        form=Sub_categoryForm()
    else:
        #post method , data is submitted
        form=Sub_categoryForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('Ecomm:Home_page')

    context={'form':form}
    return render(request,'Ecomm/add_sub_category.html',context)

    
