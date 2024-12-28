from django import forms

from .models import Category, Sub_category

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['category_name']
        labels={'category_name':''}

class Sub_categoryForm(forms.ModelForm):
    class Meta:
        model=Sub_category
        fields=['sub_category_name','category_of_subcategory']
        labels={'sub_category_name':'SubCategory','category_of_subcategory': 'Category'}


