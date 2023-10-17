from django.shortcuts import (render, redirect,
                              reverse, get_object_or_404)
from timeit import default_timer
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group, User
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
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
# Create your views here.


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
    fields = 'name', 'price', 'description', 'discount'
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return reverse(
            'shopapp:products_details',
            kwargs={'pk': self.object.pk},
        )


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'shopapp.add_product'
    # def test_func(self):
    #     # return self.request.user.groups.filter(name='secret_group').exists()
    #     return self.request.user.is_superuser

    model = Product
    fields = 'name', 'price', 'description', 'discount', 'created_by'
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