from django.shortcuts import (render, redirect,
                              reverse, get_object_or_404)
from timeit import default_timer
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

from django.contrib.auth.models import Group
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.views import View
from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from .forms import GroupForm
from django.urls import reverse_lazy, reverse
# Create your views here.


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archieved = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')

class OrderUpdateView(UpdateView):
    model = Order
    fields = 'delivery_adress', 'promocode', 'products',
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={'pk': self.object.pk}
        )

class ProductUpdateView(UpdateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return reverse(
            'shopapp:products_details',
            kwargs={'pk': self.object.pk},
        )


class ProductCreateView(CreateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    success_url = reverse_lazy('shopapp:products_list')

class ShopIndexView(View):
    def get(self, request: HttpRequest):
        products = [
            ('Laptop', 1999),
            ('Smartphone', 999),
        ]
        context = {
            'time_running':default_timer(),
            'products':products
        }
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
    


class ProductsListView(ListView):

    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archieved=False)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['products'] = Product.objects.all()
    #     return context


class OrderCreateView(CreateView):
    model = Order
    fields = 'delivery_adress', 'promocode', 'products', 'user'
    template_name_suffix = '_make_an_order'
    success_url = reverse_lazy('shopapp:orders_list')




class OrdersListView(ListView):

    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )

class OrderDetailView(DetailView):
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )