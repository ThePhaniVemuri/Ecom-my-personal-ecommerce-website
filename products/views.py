from django.shortcuts import render,redirect
from .forms import ProductForm,ProductFilterForm
from .models import Product
from users.models import Cart
from Ecomm.models import Category,Sub_category
from datetime import datetime

def Products_in_sub_category(request,sub_category_name):
    """Shows the products under the given category and its subcategories."""
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    products_in_sub_category=Product.objects.filter(product_sub_category__sub_category_name__iexact=sub_category_name)
    form = ProductFilterForm(request.GET or None, products_queryset=products_in_sub_category)
    # Apply filters if the form is valid
    if form.is_valid():
        # Filter by minimum price
        if form.cleaned_data['min_price']:
            products_in_sub_category = products_in_sub_category.filter(price__gte=form.cleaned_data['min_price'])

        # Filter by maximum price
        if form.cleaned_data['max_price']:
            products_in_sub_category = products_in_sub_category.filter(price__lte=form.cleaned_data['max_price'])

        # Filter by brand (if applicable in your Product model)
        if form.cleaned_data.get('brands'):
            products_in_sub_category = products_in_sub_category.filter(product_brand=form.cleaned_data['brands'])
    cart_items=Cart.objects.all()
    context = {'products_in_sub_category': products_in_sub_category,'form':form,'cart_items':cart_items,'Categories': categories,
        'Sub_categories': subcategories,'sub_category_name':sub_category_name}
    return render(request, 'products/products_in_sub_category.html', context)


def search_bar(request):
    """Handles search for products based on exact match, category, and partial match."""
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    searched_input = request.GET.get('q', '').strip()

    # Debug: Ensure the search term is captured
    print(f"Search term received: {searched_input}")

    # Step 1: Exact match search (case-insensitive)
    result_product1 = Product.objects.filter(product_name__iexact=searched_input)

    # Debug: Check if exact matches are found
    print(f"Exact matches found: {result_product1.count()}")

    # Step 2: Products in the same category as the first exact match
    #product_same_category = []
    if result_product1:
        # Get the category of the first exact match (if any)
        category = result_product1.first().product_category
        print(f"Category of first match: {category.category_name}")

        # Fetch products from the same category that also contain the search term
        product_same_category = Product.objects.filter(
            product_category=category,
            product_name__icontains=searched_input
        ).exclude(id__in=result_product1.values_list('id', flat=True))
    else:
        product_same_category = []

    # Step 3: Products with the search term in their name (partial match)
    other_textmatch_products = Product.objects.filter(
        product_name__icontains=searched_input
    ).exclude(id__in=result_product1.values_list('id', flat=True))

    # Debugging
    #print(f"Found {len(product_same_category)} products in the same category.")
    #print(f"Found {len(other_textmatch_products)} other text match products.")

    # Prepare context to send to the template
    context = {
        'searched_input': searched_input,
        'result_product1': result_product1,
        'product_same_category': product_same_category,
        'other_textmatch_products': other_textmatch_products,
        'Categories': categories,
        'Sub_categories': subcategories,
        #'message': None if result_product1.exists() or product_same_category.exists() or other_textmatch_products.exists() else "No products found for this search."
    }

    return render(request, 'products/search_product.html', context)
