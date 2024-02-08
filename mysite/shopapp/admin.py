from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import path

from .common import save_csv_products, save_csv_orders
from .models import Product, Order, ProductImage
from django.db.models import QuerySet
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm


@admin.action(description="Archieve products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archieved=True)

@admin.action(description="UnArchieve products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archieved=False)


class ProductInline(admin.StackedInline):
    model = ProductImage


class OrderInline(admin.TabularInline):
    model = Order.products.through


class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = 'shopapp/products_changelist.html'
    actions = [
        mark_archived,
        'export_csv',
        mark_unarchived
    ]
    inlines = [
        ProductInline,
        OrderInline,
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archieved'
    list_display_links = 'pk', 'name'
    ordering = 'pk',
    search_fields = 'name', 'description'
    fieldsets = [
        (None, {
            'fields': ('name', 'description')
        }),
        ('Price options', {
            'fields': ('price', 'discount'),
            'classes': ('collapse',)
        }),
        ('Extra options', {
            'fields': ('archieved',),
            'classes': ('collapse',),
            'description': 'Extra options. Field "archieved" is for soft delete'
        }),
        ('Images', {
            'fields': ('preview',),
        })
    ]

    def import_csv(self, request: HttpRequest):
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context=context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'admin/csv_form.html', context=context, status=400)

        save_csv_products(
            file=form.files['csv_file'].file,
            encoding=request.encoding
        )


        self.message_user(request, 'data from CSV was imported')
        return redirect('..')
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                'import-products-csv/',
                self.import_csv,
                name='import_products_csv'
            ),
        ]
        return new_urls + urls

admin.site.register(Product, ProductAdmin)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = 'shopapp/orders_changelist.html'
    inlines = [
        OrderInline,

    ]
    list_display = 'delivery_adress', 'promocode', 'created_at'
    def get_queryset(self, request):
        return Order.objects.select_related('user')

    def user_verbose(self, obj: Order):
        return obj.user.first_name or obj.user.username


    def import_csv(self, request: HttpRequest):
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context=context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'admin/csv_form.html', context=context, status=400)

        save_csv_orders(
            file=form.files['csv_file'].file,
            encoding=request.encoding
        )


        self.message_user(request, 'data from CSV was imported')
        return redirect('..')
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                'import-orders-csv/',
                self.import_csv,
                name='import_orders_csv'
            ),
        ]
        return new_urls + urls