from django.contrib import admin
from django.urls import path, include
from .views import (ShopIndexView,
                    GroupsListView,
                    ProductDelailsView,
                    ProductsListView,
                    OrdersListView,
                    OrderDetailView,
                    ProductCreateView,
                    ProductUpdateView,
                    ProductDeleteView,
                    OrderDeleteView,
                    OrderUpdateView,
                    OrderCreateView)

app_name = 'shopapp'

urlpatterns = [
    path('', ShopIndexView.as_view(), name='index'),
    path('groups/', GroupsListView.as_view(), name='groups_list'),

    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductDelailsView.as_view(), name='products_details'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/create/', ProductCreateView.as_view(), name='create_a_product'),

    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/make_order/', OrderCreateView.as_view(), name='create_an_order'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order_details'),
    path('orders/<int:pk>/delete', OrderDeleteView.as_view(), name='order_delete'),
    path('orders/<int:pk>/update', OrderUpdateView.as_view(), name='order_update'),


]
