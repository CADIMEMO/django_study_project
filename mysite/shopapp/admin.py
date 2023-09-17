from django.contrib import admin
from django.http import HttpRequest
# Register your models here.
from .models import Product, Order
from django.db.models import QuerySet
from .admin_mixins import ExportAsCSVMixin

@admin.action(description="Archieve products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archieved=True)

@admin.action(description="UnArchieve products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archieved=False)

class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        'export_csv',
        mark_unarchived
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
        })

    ]

admin.site.register(Product, ProductAdmin)

class ProductInline(admin.TabularInline):
    model = Order.products.through

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,

    ]
    list_display = 'delivery_adress', 'promocode', 'created_at'
    def get_queryset(self, request):
        return Order.objects.select_related('user')

    def user_verbose(self, obj: Order):
        return obj.user.first_name or obj.user.username


