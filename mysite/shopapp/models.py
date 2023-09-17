from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    class Meta:
        ordering = ['name', 'price']
        # db_table = 'tech_products'
        # verbose_name_plural = 'products'
    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=8)
    create_at = models.DateTimeField(auto_now_add=True)
    archieved = models.BooleanField(default=False)
    @property
    def description_short(self):
        if len(self.description) < 48:
            return self.description
        return self.description[:48] + '...'

    def __str__(self):
        return f'Product {self.pk}, name = {self.name!r}'


class Order(models.Model):
    delivery_adress = models.TextField(null=False, blank=True)
    promocode = models.CharField(max_length=28, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')


