"""
В этом модуле лежат различные django view классы и функции.

Товары, заказы и все такое и так далее.
"""
import logging

from django.contrib.syndication.views import Feed
from django.shortcuts import (render, redirect,
                              reverse, get_object_or_404)
from timeit import default_timer
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group, User
from rest_framework.response import Response

from .models import Product, Order, ProductImage
from .forms import ProductForm, OrderForm
from django.views import View
from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from .forms import GroupForm,ProductForm
from .common import save_csv_products
from django.urls import reverse_lazy, reverse
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser
from .serializers import ProductSerializer, OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import action
from csv import DictWriter
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
# Create your views here.

logger = logging.getLogger(__name__)
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
        OrderingFilter,

    ]
    search_fields = ['name', 'description']
    filterset_fields = [
        'delivery_adress',
        'user',
        'promocode',
        'products'
    ]
    ordering_fields = [
        'pk',
        'user',
        'promocode',

    ]

@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):

    """
    Полный набор представлений для действий над Product
    Полный CRUD для сущностей товара.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
        OrderingFilter,

    ]
    search_fields = ['name', 'description']
    filterset_fields = [
        'name',
        'description',
        'price',
        'discount'
    ]
    ordering_fields = [
        'pk',
        'price',
        'name',
    ]
    @extend_schema(
        summary='Get one product by id',
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description='Empty response, **product** by **ID** not found'),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)
    @action(methods=['get'], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type='text/csv')
        filename = 'products-export.csv'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name',
            'description',
            'price',
            'discount'
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()
        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })
        return response
    @action(
        detail=False,
        methods=['post'],
        parser_classes=[MultiPartParser]
    )
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES['file'].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'shopapp.delete_product'
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archieved = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class OrderDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'shopapp.delete_order'
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')

class OrderUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'shopapp.change_order'
    model = Order
    fields = 'delivery_adress', 'promocode', 'products',
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={'pk': self.object.pk}
        )




class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'shopapp.change_product'
    model = Product
    # fields = 'name', 'price', 'description', 'discount', 'preview'
    template_name_suffix = '_update_form'

    form_class = ProductForm
    def get_success_url(self):
        return reverse(
            'shopapp:products_details',
            kwargs={'pk': self.object.pk},
        )
    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.object.create(
                product=self.object,
                image=image
            )
        return response


class ProductCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):

    # permission_required = 'shopapp.add_product'
    model = Product
    # fields = 'name', 'price', 'description', 'discount', 'preview'
    form_class = ProductForm
    success_url = reverse_lazy('shopapp:products_list')



    # def test_func(self):
    #     # return self.request.user.groups.filter(name='secret_group').exists()
    #     return self.request.user.is_superuser

    # def form_valid(self, form):
    #     product = form.save(commit=False)
    #     product.created_by = self.request.user
    #     response = super().form_valid(form)
    #     return response
    #
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)



class ShopIndexView(View):
    def get(self, request: HttpRequest):
        products = [
            ('Laptop', 1999),
            ('Smartphone', 999),
        ]
        context = {
            'time_running': default_timer(),
            'products': products,
            'items': 5,
        }
        logger.debug('Products for shop index: %s', products)
        logger.info('Rendering shop index')
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest):

        context = {
            'form': GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),


        }
        return render(request, 'shopapp/groups_list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)

class ProductDelailsView(DetailView):
    template_name = 'shopapp/product-details.html'
    model = Product
    context_object_name = 'product'
    queryset = Product.objects.prefetch_related('images')
    


class ProductsListView(ListView):

    template_name = 'shopapp/products-list.html'
    model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archieved=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    # fields = _('delivery_adress'), _('promocode'), _('products')
    template_name_suffix = '_make_an_order'
    success_url = reverse_lazy('shopapp:orders_list')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)






class OrdersListView(LoginRequiredMixin, ListView):

    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )

class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order'
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )


class ProductsDataExportsView(View):

    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by('pk').all()
        products_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': product.price,
                'archieved': product.archieved,
                'created_by': str(product.created_by)

            }
            for product in products
        ]
        elem = products_data[0]
        name = elem['name']
        print('name:', name)
        return JsonResponse({'products': products_data})


class OrdersDataExportView(View):

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.all()
        orders_data = [
            {
                'pk': order.pk,
                'delivery_adress': order.delivery_adress,
                'promocode': order.promocode,
                'user': order.user.pk,
                'products': [product.pk for product in order.products.all()]
            }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})

class LatestProductsFeed(Feed):

    title = 'Products'
    description = ''
    link = reverse_lazy('shopapp:products_list')

    def items(self):
        return (
            Product.objects
            .all()
        )
    def item_name(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]