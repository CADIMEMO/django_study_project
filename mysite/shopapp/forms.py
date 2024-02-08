from django import forms
from django.core import validators
from .models import Product, Order
from django.contrib.auth.models import Group
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = _('delivery_adress'), _('promocode'), _('products')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [_('name'), _('price'), _('description'), _('discount'), _('preview')]

    images = forms.ImageField(
        widget=forms.ClearableFileInput({'multiple': False})
    )

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()