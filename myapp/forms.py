from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Products,ProductOut

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username","email","password1","password2"]


class ProductForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, required=True)
    
    class Meta:
        model = Products
        fields = ['name','price','quantity']

