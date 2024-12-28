from django import forms
from .models import Product
from Ecomm.models import Category

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['product_name','product_category','product_sub_category','price','about_product','product_brand']
        labels={'product_name':'Product Name(in detail)','product_category':'Category Product Belongs To','product_sub_category':'Sub-Category the product belongs to','price':'Price declared for the product','about_product':'About/More on product','product_brand':'Brand of the Product'}

class ProductFilterForm(forms.Form):
    # Checkbox for categories
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),  # All available categories
        widget=forms.CheckboxSelectMultiple,  # Render as checkboxes
        required=False  # Optional
    )
    
    # Range slider for price (min and max price fields)
    min_price = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Min Price'}),
        required=False
    )
    max_price = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Max Price'}),
        required=False
    )
    
    # Dropdown for brands (you can populate options dynamically)
    brands = forms.ChoiceField(
        choices=[],  # Replace with actual brands
        widget=forms.Select,
        required=False
    )
    def __init__(self, *args, **kwargs):
        # Get the queryset of products passed from the view
        products_queryset = kwargs.pop('products_queryset', None)
        super().__init__(*args, **kwargs)

        # Dynamically set brand choices based on products_queryset
        if products_queryset is not None:
            distinct_brands = products_queryset.values_list('product_brand', flat=True).distinct()
            self.fields['brands'].choices = [(brand, brand) for brand in distinct_brands]
 

