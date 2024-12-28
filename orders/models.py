from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from products.models import Product

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)  # Buyer placing the order
    products = models.ManyToManyField(Product, through='OrderProduct')  # Many-to-many relationship with a through model
    #quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[  # Order status
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        if self.pk:  # Only calculate total_price if the Order already has a primary key
            self.total_price = sum(order_product.product.price * order_product.quantity for order_product in self.orderproduct_set.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.buyer.username}"

# Through model to handle multiple products in an order with quantities
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Product {self.product.product_name} in Order {self.order.id}"
