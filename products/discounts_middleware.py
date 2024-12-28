from products.models import Product
from datetime import datetime

class DiscountsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.discounted_products = self.get_discounted_products()
        response = self.get_response(request)
        return response

    def get_discounted_products(self):
        discounted_products = []
        electronics_products = Product.objects.filter(product_category__category_name='Electronics')
        current_time = datetime.now()

        for product in electronics_products:
            if current_time.month == 12 and current_time.day == 27:  # Today's date
                product.discounted_price = product.price * 0.8  # Apply 20% discount
            else:
                product.discounted_price = None
            discounted_products.append(product)

        return discounted_products
