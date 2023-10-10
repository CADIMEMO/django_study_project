from django import forms
from django.core import validators
from .models import Product, Order
from django.contrib.auth.models import Group
from django.forms import ModelForm


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'delivery_adress', 'promocode', 'products', 'user'