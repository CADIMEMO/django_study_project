from typing import Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product
from django.db import transaction


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Start demo bulk actions')
        info = [
            ('Smarphone 1', 199),
            ('Smarphone 2', 299),
            ('Smarphone 3', 399),
        ]
        products = [
            Product(name=name, price=price)
            for name, price in info
        ]

        result = Product.objects.bulk_create(products)
        for obj in result:
            print(obj)

        self.stdout.write('Done')