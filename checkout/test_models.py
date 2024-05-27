from decimal import Decimal
from django.test import TestCase
from django.conf import settings
from django.db.models import Sum
from django_countries.fields import Country
from products.models import Product, Category
from profiles.models import UserProfile, User
from checkout.models import Order, OrderLineItem


class OrderModelTests(TestCase):
    """
    Test cases for the Order model to ensure it behaves correctly.
    """

    def setUp(self):
        """
        Set up the initial data for the Order model tests.
        """

        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.category = Category.objects.create(name='test_category')
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            price=Decimal('10.00'),
        )
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            full_name='John Doe',
            email='john@example.com',
            phone_number='1234567890',
            country=Country(code='US'),
            town_or_city='Test City',
            street_address1='123 Test St',
            original_bag='{}',
            stripe_pid='test_stripe_pid',
        )

    def test_order_creation(self):
        """
        Test that an order instance is created correctly.
        """

        self.assertIsInstance(self.order, Order)
        self.assertIsNotNone(self.order.order_number)
        self.assertEqual(self.order.user_profile, self.user_profile)

    def test_order_number_generation(self):
        """
        Test that the order number is generated and
        remains the same upon saving.
        """

        order_number = self.order.order_number
        self.order.save()
        self.assertEqual(self.order.order_number, order_number)

    def test_update_total(self):
        """
        Test the update_total method to ensure order
        totals are calculated correctly.
        """

        OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
        )
        self.order.update_total()
        self.assertEqual(self.order.order_total, Decimal('20.00'))
        expected_delivery = Decimal('20.00') * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / Decimal('100.00')
        self.assertEqual(self.order.delivery_cost, expected_delivery)
        self.assertEqual(self.order.grand_total, self.order.order_total + self.order.delivery_cost)

    def test_free_delivery(self):
        """
        Test that orders qualifying for free delivery
        have zero delivery cost.
        """

        OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=20,
        )
        self.order.update_total()
        self.assertEqual(self.order.order_total, Decimal('200.00'))
        self.assertEqual(self.order.delivery_cost, Decimal('0.00'))
        self.assertEqual(self.order.grand_total, self.order.order_total)

    def test_order_string_representation(self):
        """
        Test the string representation of the order instance.
        """

        self.assertEqual(str(self.order), self.order.order_number)


class OrderLineItemModelTests(TestCase):
    """
    Test cases for the OrderLineItem model to ensure it behaves correctly.
    """

    def setUp(self):
        """
        Set up the initial data for the OrderLineItem model tests.
        """

        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.category = Category.objects.create(name='test_category')
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            price=Decimal('10.00'),
        )
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            full_name='John Doe',
            email='john@example.com',
            phone_number='1234567890',
            country=Country(code='US'),
            town_or_city='Test City',
            street_address1='123 Test St',
            original_bag='{}',
            stripe_pid='test_stripe_pid',
        )

    def test_order_line_item_creation(self):
        """
        Test that an order line item is created correctly.
        """

        line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
        )
        self.assertIsInstance(line_item, OrderLineItem)
        self.assertEqual(line_item.lineitem_total, Decimal('20.00'))

    def test_order_total_update_on_lineitem_save(self):
        """
        Test that the order total updates correctly when a line item is saved.
        """

        line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
        )
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_total, Decimal('20.00'))

    def test_order_line_item_string_representation(self):
        """
        Test the string representation of the order line item instance.
        """

        line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
        )
        self.assertEqual(str(line_item), f'SKU {self.product.sku} on order {self.order.order_number}')
