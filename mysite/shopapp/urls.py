from django.contrib import admin
from django.urls import path, include
from .views import shop_index, groups_list, products_list, orders_list, create_product, create_an_order
app_name = 'shopapp'

urlpatterns = [
    path('', shop_index, name='index'),
    path('groups/', groups_list, name='groups_list'),
    path('products/', products_list, name='products_list'),
    path('orders/', orders_list, name='orders_list'),
    path('create/', create_product, name='create_product'),
    path('orders/make_order/', create_an_order, name='create_an_order')

]
