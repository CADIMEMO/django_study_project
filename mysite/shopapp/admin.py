from django.contrib import admin
from django.http import HttpRequest
from .models import Product, Order, ProductImage
from django.db.models import QuerySet
from .admin_mixins import ExportAsCSVMixin

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


admin.site.register(Product, ProductAdmin)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderInline,

    ]
    list_display = 'delivery_adress', 'promocode', 'created_at'
    def get_queryset(self, request):
        return Order.objects.select_related('user')

    def user_verbose(self, obj: Order):
        return obj.user.first_name or obj.user.username


