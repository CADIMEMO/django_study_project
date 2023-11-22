from typing import Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Min, Count, Sum

from shopapp.models import Order, Product
from django.db import transaction


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Start demo agg')
        result = Product.objects.aggregate(
            Avg('price'),
            Max('price'),
            Min('price'),
            Count('id')
        )
        print(result)

        orders = Order.objects.annotate(
            total=Sum('products__price', default=0),
            products_count=Count('products')
        )
        for order in orders:
            print(
                f'Order #{order.id} '
                f'With {order.products_count} '
                f'products worth {order.total}'
            )

        self.stdout.write('Done')