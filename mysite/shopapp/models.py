from django.db import models
from django.contrib.auth.models import User
from  django.utils.translation import gettext_lazy as _


# Create your models here.

def product_preview_directory_path(instance: 'Product', filename: str) -> str:
    return 'products/product_{pk}/preview/{filename}'.format(
        pk=instance.pk,
        filename=filename

    )

class Product(models.Model):
    class Meta:
        ordering = ['name', 'price']
        # verbose_name = _('Product')
    verbose_name = _('Product')
    verbose_name_plural = _('Products')
    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=8)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    create_at = models.DateTimeField(auto_now_add=True)
    archieved = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)

    @property
    def description_short(self):
        if len(self.description) < 48:
            return self.description
        return self.description[:48] + '...'

    def __str__(self):
        return f'Product {self.pk}, name = {self.name!r}'

def product_images_directory_path(instance: 'ProductImage', filename=str):
    return 'products/product_{pk}/images/{filename}'.format(
        pk=instance.product.pk,
        filename=filename
    )

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=255, null=False, blank=True)

class Order(models.Model):
    verbose_name = _('Order')
    verbose_name_plural = _('Orders')
    delivery_adress = models.TextField(null=False, blank=True)
    promocode = models.CharField(max_length=28, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')
    reciept = models.FileField(null=True, upload_to='orders/reciepts')


