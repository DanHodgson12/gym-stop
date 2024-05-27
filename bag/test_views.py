from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
from products.models import Product, Category


class BagViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='test_category')
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            price=10.00,
        )
        self.bag_url = reverse('view_bag')
        self.add_to_bag_url = reverse('add_to_bag', args=[self.product.id])
        self.adjust_bag_url = reverse('adjust_bag', args=[self.product.id])
        self.remove_from_bag_url = reverse('remove_from_bag', args=[self.product.id])

    def test_view_bag(self):
        """
        Test viewing the bag page.
        """

        response = self.client.get(self.bag_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')

    def test_add_to_bag(self):
        """
        Test adding a product to the bag.
        """

        response = self.client.post(self.add_to_bag_url, {
            'quantity': 1,
            'redirect_url': self.bag_url
        })
        self.assertRedirects(response, self.bag_url)
        session = self.client.session
        self.assertIn(str(self.product.id), session['bag'])
        self.assertEqual(session['bag'][str(self.product.id)], 1)

    def test_add_to_bag_with_size(self):
        """
        Test adding a product with size to the bag.
        """

        response = self.client.post(self.add_to_bag_url, {
            'quantity': 1,
            'product_size': 'M',
            'redirect_url': self.bag_url
        })
        self.assertRedirects(response, self.bag_url)
        session = self.client.session
        self.assertIn(str(self.product.id), session['bag'])
        self.assertIn('M', session['bag'][str(self.product.id)]['items_by_size'])
        self.assertEqual(session['bag'][str(self.product.id)]['items_by_size']['M'], 1)

    def test_adjust_bag(self):
        """
        Test adjusting the quantity of a product in the bag.
        """

        session = self.client.session
        session['bag'] = {str(self.product.id): 1}
        session.save()
        response = self.client.post(self.adjust_bag_url, {'quantity': 2})
        self.assertRedirects(response, self.bag_url)
        session = self.client.session
        self.assertEqual(session['bag'][str(self.product.id)], 2)

    def test_adjust_bag_with_size(self):
        """
        Test adjusting the quantity of a product with size in the bag.
        """

        session = self.client.session
        session['bag'] = {str(self.product.id): {'items_by_size': {'M': 1}}}
        session.save()
        response = self.client.post(self.adjust_bag_url, {'quantity': 2, 'product_size': 'M'})
        self.assertRedirects(response, self.bag_url)
        session = self.client.session
        self.assertEqual(session['bag'][str(self.product.id)]['items_by_size']['M'], 2)

    def test_remove_from_bag(self):
        """
        Test removing a product from the bag.
        """

        session = self.client.session
        session['bag'] = {str(self.product.id): 1}
        session.save()
        response = self.client.post(self.remove_from_bag_url)
        self.assertEqual(response.status_code, 200)
        session = self.client.session
        self.assertNotIn(str(self.product.id), session['bag'])

    def test_remove_from_bag_with_size(self):
        """
        Test removing a product with size from the bag.
        """

        session = self.client.session
        session['bag'] = {str(self.product.id): {'items_by_size': {'M': 1}}}
        session.save()
        response = self.client.post(self.remove_from_bag_url, {'product_size': 'M'})
        self.assertEqual(response.status_code, 200)
        session = self.client.session
        self.assertNotIn(str(self.product.id), session['bag'])
