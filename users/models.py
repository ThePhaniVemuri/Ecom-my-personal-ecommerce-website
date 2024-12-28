from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user owning the cart
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Product in the cart
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product

    def __str__(self):
        return f"{self.user.username}'s cart - {self.product.product_name} ({self.quantity})"

    def get_total_price(self):
        """Calculate the total price for this cart item"""
        return self.product.price * self.quantity

