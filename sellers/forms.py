from django import forms
from django.contrib.auth.models import User

class SellerRegistrationForm(forms.ModelForm):
    store_name = forms.CharField(max_length=100)  # Extra field for store name
    address = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
