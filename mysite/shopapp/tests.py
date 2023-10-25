from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.test import TestCase
from random import choices
from django.urls import reverse
from string import ascii_letters

from .models import Product, Order
from .utils import add_two_numbers
# Create your tests here.


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEquals(result, 5)


class ProductCreateViewTestCase(TestCase):


    def setUp(self):
        self.user = User.objects.create_user(username='TestUserProductCreate', password='qwerty123')
        self.product_name = ''.join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()


    def test_create_product(self):
        self.client.login(username='TestUserProductCreate', password='qwerty123')
        response = self.client.post(
            reverse('shopapp:create_a_product'),
            {
                'name': self.product_name,
                'price': '123.45',
                'description': 'A good table',
                'discount': '8',
                'created_by': self.user

            }
        )
        self.assertRedirects(response, reverse('shopapp:products_list'))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )



class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='TestAdmin1', password='qwerty123')
        cls.user.user_permissions.add(28)
        cls.product = Product.objects.create(name='Best product', created_by=cls.user)

    def setUp(self):
        self.client.login(username='TestAdmin1', password='qwerty123')

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        cls.user.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse('shopapp:products_details',
                    kwargs={'pk': self.product.pk}
                    )
        )
        self.assertEquals(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse('shopapp:products_details',
                    kwargs={'pk': self.product.pk}
                    )
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):

    fixtures = [
        'products-fixture.json',
        'profiles-fixture.json'
    ]

    def test_products(self):
        response = self.client.get(reverse('shopapp:products_list'))
        for product in Product.objects.filter(archieved=False).all():
            self.assertContains(response, product.name)


class OrderListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='TestAdmin',
                               password='12345678')
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.login(**self.credentials)

    def test_orders_view(self):
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertContains(response, 'Orders')

    def test_orders_vies_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertEquals(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
        'profiles-fixture.json'
    ]

    def test_get_products_view(self):
        response = self.client.get(reverse('shopapp:products-export'))
        self.assertEquals(response.status_code, 200)
        products = Product.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': str(product.price),
                'archieved': product.archieved,
                'created_by': str(product.created_by)
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEquals(
            products_data['products'],
            expected_data
        )


class OrderDetailTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = {
            'username': 'TestOrderDetailsUser',
            'password': 'qwerty123',


        }
        cls.user = User.objects.create_user(**cls.credentials)
        cls.product = Product.objects.create(name='TestProduct', created_by=cls.user)
        cls.order = Order.objects.create(delivery_adress='TestAdress',
                                         promocode='123test',
                                         created_at=models.DateTimeField(auto_now_add=True),
                                         user=cls.user,

                                         )
        cls.order.products.set(str(cls.product.pk))
        cls.user.user_permissions.add(32)

    def setUp(self):
        self.client.login(**self.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.order.delete()
        cls.product.delete()
        cls.user.delete()

    def test_get_order_details(self):

        response = self.client.get(reverse('shopapp:order_details', kwargs={'pk': self.order.pk}))
        self.assertEquals(response.status_code, 200)

        self.assertContains(response, self.order.delivery_adress)
        self.assertContains(response, self.order.promocode)
        self.assertContains(response, self.order.pk)


class OrdersDataExportTestCase(TestCase):
    fixtures = ['orders-fixture.json',
                'profiles-fixture.json',
                'products-fixture.json']
    def test_export_data(self):
        response = self.client.get(reverse('shopapp:orders-export'))
        orders = Order.objects.all()
        expected_data = [
            {

                'pk': order.pk,
                'delivery_adress': order.delivery_adress,
                'promocode': order.promocode,
                'user': str(order.user),
                'products': str(order.products)
            }
            for order in orders
        ]
        response_data = response.json()
        self.assertEquals(response_data['orders'], expected_data)

