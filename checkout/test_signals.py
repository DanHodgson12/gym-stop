from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from decimal import Decimal
from products.models import Product
from checkout.models import Order, OrderLineItem


User = get_user_model()


class SignalsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('10.00')
        )
        self.order = Order.objects.create(
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='US',
            postcode='12345',
            town_or_city='Test City',
            street_address1='123 Test St',
            street_address2='',
            county='Test County',
        )

    def test_update_on_save_signal(self):
        """
        Test that the update_on_save signal updates the order total
        when an order line item is saved.
        """
        OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
        )
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_total, Decimal('10.00'))
        self.assertEqual(self.order.delivery_cost, Decimal('1.00'))
        self.assertEqual(self.order.grand_total, Decimal('11.00'))

    def test_update_on_delete_signal(self):
        """
        Test that the update_on_delete signal updates the order total
        when an order line item is deleted.
        """
        line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
        )
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_total, Decimal('10.00'))
        self.assertEqual(self.order.delivery_cost, Decimal('1.00'))
        self.assertEqual(self.order.grand_total, Decimal('11.00'))

        line_item.delete()
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_total, Decimal('0.00'))
        self.assertEqual(self.order.delivery_cost, Decimal('0.00'))
        self.assertEqual(self.order.grand_total, Decimal('0.00'))
