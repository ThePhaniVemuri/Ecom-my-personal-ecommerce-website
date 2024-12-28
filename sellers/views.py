from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Seller
from Ecomm.models import Category,Sub_category
from orders.models import OrderProduct
from .forms import SellerRegistrationForm
from products.forms import ProductForm

def register_seller(request):
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the User
            Seller.objects.create(user=user, store_name=form.cleaned_data['store_name'])  # Create Seller
            return redirect('sellers:seller_login')  # Redirect to login
    else:
        form = SellerRegistrationForm()
    return render(request, 'sellers/register.html', {'form': form,'Categories': categories,
        'Sub_categories': subcategories,})

class SellerLoginView(LoginView):
    template_name = 'sellers/seller_login.html'

    def form_valid(self, form):
        """Check if the user is a seller before allowing login."""
        user = form.get_user()
        try:
            # Check if the user is linked to a Seller profile
            user.seller
        except Seller.DoesNotExist:
            # If not a seller, show an error and redirect to the login page
            messages.error(self.request, "You are not registered as a seller.")
            return redirect('sellers:seller_login')  # Adjust to your seller login URL
        
        return super().form_valid(form)  # Allow login if the user is a seller

def logoutt(request):
    """To logout of page"""
    logout(request)
    return redirect('Ecomm:Home_page')

def is_seller(user):
    return hasattr(user, 'seller')  # Check if the user is linked to a Seller

@login_required
@user_passes_test(is_seller)
def add_product(request):
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller  # Link the product to the seller
            product.save()
            return redirect('sellers:dashboard')  # Redirect to the seller's dashboard
    else:
        form = ProductForm()
    return render(request, 'sellers/add_product.html', {'form': form,'Categories': categories,
        'Sub_categories': subcategories,})

@login_required
@user_passes_test(is_seller)
def dashboard(request):
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    seller = request.user.seller
    products = seller.products.all()  # All products added by this seller
    orders = OrderProduct.objects.filter(product__seller=seller)  # Orders for this seller's products
    return render(request, 'sellers/dashboard.html', {'products': products, 'orders': orders,'Categories': categories,
        'Sub_categories': subcategories,})

@login_required
@user_passes_test(is_seller)
def manage_orders(request):
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    seller = request.user.seller
    orders = OrderProduct.objects.filter(product__seller=seller)
    return render(request, 'sellers/manage_orders.html', {'orders': orders,'Categories': categories,
        'Sub_categories': subcategories,})






