from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch, Mock
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
from django.contrib.messages import get_messages


class CheckoutViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass')
        self.product = Product.objects.create(
            name='Test Product', price=10.00, sku='testsku')
        self.order = Order.objects.create(
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='US',
            postcode='12345',
            town_or_city='Test Town',
            street_address1='123 Test St',
            street_address2='',
            county='Test County',
            original_bag='{}',
            stripe_pid='test_pid',
        )
        self.order_line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            lineitem_total=10.00,
        )

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_view_get(self, mock_create):
        mock_create.return_value = Mock(client_secret='test_secret')
        self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['bag'] = {str(self.product.id): 1}
        session.save()
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_view_post_valid(self, mock_create):
        mock_create.return_value = Mock(client_secret='test_secret')
        self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['bag'] = {str(self.product.id): 1}
        session.save()
        form_data = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'country': 'US',
            'postcode': '12345',
            'town_or_city': 'Test Town',
            'street_address1': '123 Test St',
            'street_address2': '',
            'county': 'Test County',
            'client_secret': 'test_pid_secret',
        }
        response = self.client.post(reverse('checkout'), form_data)
        order = Order.objects.last()
        self.assertRedirects(response, reverse('checkout_success', args=[order.order_number]))

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_view_post_invalid(self, mock_create):
        mock_create.return_value = Mock(client_secret='test_secret')
        self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['bag'] = {str(self.product.id): 1}
        session.save()
        form_data = {
            'full_name': '',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'country': 'US',
            'postcode': '12345',
            'town_or_city': 'Test Town',
            'street_address1': '123 Test St',
            'street_address2': '',
            'county': 'Test County',
            'client_secret': 'test_pid_secret',
        }
        response = self.client.post(reverse('checkout'), form_data)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]).replace(' ', ''), 'Therewasanerrorwithyourform.Pleasedoublecheckyourinformation.')

    def test_checkout_success_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('checkout_success', args=[self.order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Order successfully processed!', str(messages[0]))

    @patch('checkout.views.stripe.PaymentIntent.modify')
    def test_cache_checkout_data_view(self, mock_modify):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('cache_checkout_data'), {
            'client_secret': 'test_pid_secret',
            'save_info': True,
        })
        self.assertEqual(response.status_code, 200)

    @patch('checkout.views.stripe.PaymentIntent.modify')
    def test_cache_checkout_data_view_exception(self, mock_modify):
        mock_modify.side_effect = Exception('Test Error')
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('cache_checkout_data'), {
            'client_secret': 'test_pid_secret',
            'save_info': True,
        })
        self.assertEqual(response.status_code, 400)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]).replace(' ', ''), 'Sorry,yourpaymentcannotbeprocessedrightnow.Pleasetryagainlater.')
