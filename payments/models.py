from django.db import models
from django.contrib.auth.models import User
#from orders.models import Order

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE)  # Link to order
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phonepe_transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')  # Pending, Success, Failed
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id} - {self.status}"
