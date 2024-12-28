from django.db import models
from django.utils import timezone

class Product(models.Model):
    """For the products list"""
    product_category=models.ForeignKey('Ecomm.Category',on_delete=models.CASCADE)
    product_sub_category=models.ForeignKey('Ecomm.Sub_category',on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey('sellers.Seller', on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    product_name=models.CharField(max_length=300)
    about_product=models.TextField()
    price=models.IntegerField()
    product_brand=models.CharField(max_length=300, null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    #image=models.ImageField()
    #reviews=models.TextField()
    def __str__(self):
        return f"{self.product_name} ({self.product_category.category_name})"
#class Review(models.Model):
#    """link this to the product"""
    
    
    
