from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
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
                    OrderCreateView,
                    ProductsDataExportsView,
                    OrdersDataExportView,
                    ProductViewSet,
                    OrderViewSet,
                    LatestProductsFeed,
                    export_orders_csv,
                    UserOrdersDetailView,
                    UserOrdersDataExportView)
from django.views.decorators.cache import cache_page

app_name = 'shopapp'

routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)

urlpatterns = [
    path('', cache_page(60)(ShopIndexView.as_view()), name='index'),
    path('groups/', GroupsListView.as_view(), name='groups_list'),

    path('api/', include(routers.urls)),

    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/export/', ProductsDataExportsView.as_view(), name='products-export'),
    path('products/<int:pk>/', ProductDelailsView.as_view(), name='products_details'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/create/', ProductCreateView.as_view(), name='create_a_product'),
    path('products/feed', LatestProductsFeed(), name='products_feed'),

    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/make_order/', OrderCreateView.as_view(), name='create_an_order'),
    path('orders/export/', OrdersDataExportView.as_view(), name='orders-export'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order_details'),
    path('orders/<int:pk>/delete', OrderDeleteView.as_view(), name='order_delete'),
    path('orders/<int:pk>/update', OrderUpdateView.as_view(), name='order_update'),
    # path('orders/orders_list_of_user', UserOrdersDetailView.as_view(), name='user_orders_list'),
    path('users/<int:pk>/orders', UserOrdersDetailView.as_view(), name='user_orders_list'),
    path('users/<int:pk>/orders/export', UserOrdersDataExportView.as_view(), name='user_orders_export'),

    path('export', export_orders_csv, name='export_orders_csv')



]
