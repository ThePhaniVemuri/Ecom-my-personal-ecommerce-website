from django.db import models
from django.contrib.auth.models import User

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='seller')  # Link to User model
    store_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.store_name

