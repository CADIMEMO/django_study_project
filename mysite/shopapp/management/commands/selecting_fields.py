from typing import Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product
from django.db import transaction


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Start demo select fields')
        users_info = User.objects.values_list('username', flat=True)
        print(list(users_info))
        for info in users_info:
            print(info)
        # product_values = Product.objects.values('pk', 'name')
        # for p_values in product_values:
        #     print(p_values)

        self.stdout.write('Done')