from django.db import models

class Category(models.Model):
    """Shows the category name which contains products"""
    category_name=models.CharField(max_length=100)

    def __str__(self):
        """Return the name of category as string"""
        return self.category_name

class Sub_category(models.Model):
    """Shows the sub_category"""
    category_of_subcategory=models.ForeignKey('Category',on_delete=models.CASCADE)
    sub_category_name=models.CharField(max_length=100, null=True, blank=True)    

    def __str__(self):
        """Return the name of sub_category as string"""
        return self.sub_category_name    
