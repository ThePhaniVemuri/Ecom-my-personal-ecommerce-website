from django.shortcuts import render,redirect,get_object_or_404
from .models import Order,OrderProduct
from django.contrib.auth.decorators import login_required, user_passes_test
from products.models import Product
from users.models import Cart
from Ecomm.models import Category,Sub_category

@login_required
def place_order(request, product_id):
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not provided
        if quantity < 1:
            quantity = 1
        # Create an order and associate the product with the quantity
        order = Order.objects.create(buyer=request.user, status='Pending')
        OrderProduct.objects.create(order=order, product=product, quantity=quantity)
        return redirect('orders:order_history')

    return render(request, 'orders/place_order.html', {'product': product,'Categories': categories,
        'Sub_categories': subcategories,})

@login_required
def order_history(request):
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    orders = Order.objects.filter(buyer=request.user).order_by('-order_date')
    cart_items = Cart.objects.filter(user=request.user)
    total_price=total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'orders/order_history.html', {'orders': orders,'total_price':total_price,'Categories': categories,
        'Sub_categories': subcategories,})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    if order.status == 'Pending':  # Only allow cancellation for pending orders
        order.status = 'Cancelled'
        order.save()
    return redirect('orders:order_history')


