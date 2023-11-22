from typing import Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product
from django.db import transaction
class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Create order with products')
        user = User.objects.get(username='admin')
        products: Sequence[Product] = Product.objects.defer('description', 'price').all()
        order, created = Order.objects.get_or_create(delivery_adress='ul Orj dom 11',
                                            promocode='Cake1234',
                                            user=user
                                            )

        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(f'Create order {order}')

