from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Cart
from products.models import Product
from Ecomm.models import Category,Sub_category
from orders.models import Order,OrderProduct

def register(request):
    """Register new user."""
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    if request.method!='POST':
        #no data submitted so blank form
        form=UserCreationForm()
    else:
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            login(request,new_user)
            return redirect('Ecomm:Home_page')
    context={'form':form,'Categories': categories,
        'Sub_categories': subcategories,}
    return render(request,'registration/register.html',context)

def logoutt(request):
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    """To logout of page"""
    logout(request)
    return redirect('Ecomm:Home_page')


@login_required
def add_to_cart(request, product_id):
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    """Add a product to the cart or update quantity if already present."""
    product = get_object_or_404(Product, id=product_id)
    #order_quantity = get_object_or_404(Order, product__id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1  # Increment quantity if the product is already in the cart
    cart_item.save()
    return redirect('users:view_cart')  # Redirect to the cart page

@login_required
def view_cart(request):
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    """Display all items in the user's cart."""
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)  # Calculate total cart price
    orders = Order.objects.filter(buyer=request.user, status="Pending") 
    return render(request, 'users/view_cart.html', {'cart_items': cart_items, 'total_price': total_price,'orders': orders,'Categories': categories,
        'Sub_categories': subcategories,})

@login_required
def update_cart(request, cart_item_id):
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    """Update the quantity of a product in the cart."""
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)

    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', cart_item.quantity))
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove the item if quantity is set to 0
    return redirect('users:view_cart')

@login_required
def remove_from_cart(request, cart_item_id):
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    """Remove an item from the cart."""
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('users:view_cart')

@login_required
def checkout(request):
    total_price=0
    """Convert cart items to orders and clear the cart."""
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    cart_items = Cart.objects.filter(user=request.user)
    orders = []  # To store the created orders
    for item in cart_items:
        order = Order(buyer=request.user, status='Pending')
        order.save()
        # Add the product(s) in the cart item to the order with the quantity
        order_product = OrderProduct.objects.create(
            order=order,
            product=item.product,  # Assuming `Cart` has a `product` field
            quantity=item.quantity
        )
        order.save()
        # Append the created order to the list of orders
        orders.append(order)
    # Clear the user's cart
    total_price = sum(item.get_total_price() for item in cart_items)
    order_ids= ','.join([str(order.id) for order in orders])
    cart_items.delete()
    # Redirect to the payment page with the created orders
    return render(request, 'payments/check_out.html', {'orders': orders, 'total_price': total_price,'Categories': categories,
        'Sub_categories': subcategories,'order_ids':order_ids})#redirect('payments:initiate_payment', order_ids=','.join([str(order.id) for order in orders]))




        
