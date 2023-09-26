from django.shortcuts import render, redirect, reverse
from timeit import default_timer
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import Group
from .models import Product, Order
from .forms import ProductForm, OrderForm
# Create your views here.
def shop_index(request):
    products = [
        ('Laptop', 1999),
        ('Smartphone', 999),
    ]
    context = {
        'time_running':default_timer(),
        'products':products
    }
    return render(request, 'shopapp/shop-index.html', context=context)

def groups_list(request: HttpRequest):
    context = {
        "groups": Group.objects.prefetch_related('permissions').all(),


    }
    return render(request, 'shopapp/groups_list.html', context=context)

def products_list(request: HttpRequest):

    context = {
        'products': Product.objects.all()

    }

    return render(request, 'shopapp/products-list.html', context=context)

def orders_list(request: HttpRequest):

    context = {
        'orders': Order.objects.select_related('user').all(),



    }
    return render(request, 'shopapp/orders-list.html', context=context)

def create_product(request: HttpRequest):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():

            # Product.objects.create(**form.cleaned_data)
            form.save()
            url = reverse('shopapp:products_list')
            return redirect(url)
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'shopapp/create-product.html', context=context)

def create_an_order(request: HttpRequest):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse('shopapp:orders_list')
            return redirect(url)
    else:
        form = OrderForm()
    context = {
        'form': form,
    }
    return render(request, 'shopapp/make-order.html', context=context)
