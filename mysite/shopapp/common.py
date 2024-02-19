from csv import DictReader
from io import TextIOWrapper

from shopapp.models import Product, Order


def save_csv_products(file, encoding):

    csv_file = TextIOWrapper(
        file,
        encoding
    )
    reader = DictReader(csv_file)

    products = [
        Product(**row)
        for row in reader
    ]
    Product.objects.bulk_create(products)
    return products

def save_csv_orders(file, encoding):

    csv_file = TextIOWrapper(
        file,
        encoding
    )
    reader = DictReader(csv_file)

    # orders = [
    #     Order(**row)
    #     for row in reader
    # ]
    # Order.objects.bulk_create(orders)
    # return orders

    for row in reader:
        products = row.pop('products')
        order = Order(**row)
        order.save()
        products_ids = []
        for sym in products:
            if sym in '1234567890':
                products_ids.append(int(sym))
        order.products.set(products_ids)


