from decimal import Decimal
from django.test import TestCase, RequestFactory
from django.conf import settings
from products.models import Product, Category
from bag.contexts import bag_contents


class BagContextsTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name='test_category')
        self.product1 = Product.objects.create(
            name='Test Product 1',
            category=self.category,
            price=Decimal('10.00'),
        )
        self.product2 = Product.objects.create(
            name='Test Product 2',
            category=self.category,
            price=Decimal('20.00'),
            has_sizes=True
        )

    def test_bag_contents_no_items(self):
        """
        Test bag_contents with no items in the session bag.
        """

        request = self.factory.get('/')
        request.session = {}
        context = bag_contents(request)
        self.assertEqual(context['total'], Decimal('0.00'))
        self.assertEqual(context['product_count'], 0)
        self.assertEqual(len(context['bag_items']), 0)
        self.assertEqual(context['delivery'], Decimal('0.00'))
        self.assertEqual(context['free_delivery_delta'], Decimal(settings.FREE_DELIVERY_THRESHOLD).quantize(Decimal('0.00')))
        self.assertEqual(context['grand_total'], Decimal('0.00'))

    def test_bag_contents_with_items(self):
        """
        Test bag_contents with multiple items, including
        items with sizes, in the session bag.
        """

        request = self.factory.get('/')
        request.session = {
            'bag': {
                str(self.product1.id): 2,
                str(self.product2.id): {
                    'items_by_size': {
                        'M': 1,
                        'L': 3
                    }
                }
            }
        }
        context = bag_contents(request)
        expected_total = (Decimal('10.00') * 2 + Decimal('20.00') * (1 + 3)).quantize(Decimal('0.00'))
        self.assertEqual(context['total'], expected_total)
        self.assertEqual(context['product_count'], 6)
        self.assertEqual(len(context['bag_items']), 3)
        self.assertEqual(context['delivery'], Decimal('0.00'))
        self.assertEqual(context['free_delivery_delta'], Decimal('0.00'))
        self.assertEqual(context['grand_total'], expected_total)

    def test_bag_contents_with_delivery(self):
        """
        Test bag_contents with an item in the session bag
        that incurs a delivery charge.
        """

        request = self.factory.get('/')
        request.session = {
            'bag': {
                str(self.product1.id): 1
            }
        }
        context = bag_contents(request)
        total = Decimal('10.00')
        delivery_percentage = Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / Decimal('100.00')
        delivery = (total * delivery_percentage).quantize(Decimal('0.00'))
        grand_total = (total + delivery).quantize(Decimal('0.00'))
        free_delivery_delta = (Decimal(settings.FREE_DELIVERY_THRESHOLD) - total).quantize(Decimal('0.00'))

        self.assertEqual(context['total'], total.quantize(Decimal('0.00')))
        self.assertEqual(context['product_count'], 1)
        self.assertEqual(len(context['bag_items']), 1)
        self.assertEqual(context['delivery'], delivery)
        self.assertEqual(context['free_delivery_delta'], free_delivery_delta)
        self.assertEqual(context['grand_total'], grand_total)
