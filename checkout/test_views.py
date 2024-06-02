from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from products.models import Product
from profiles.models import UserProfile
from checkout.models import Order, OrderLineItem
from django.contrib.auth.models import User
from checkout.forms import OrderForm
from unittest.mock import patch, Mock


class CheckoutViewsTests(TestCase):
    """
    Test cases for the views in the checkout app.
    """

    def setUp(self):
        """
        Set up the initial data for the checkout view tests.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass'
        )
        self.product = Product.objects.create(
            name='Test Product', price=10.00, sku='testsku'
        )
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
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_view_get(self, mock_create):
        """
        Test the GET method of the checkout view.
        """
        mock_create.return_value = Mock(client_secret='test_secret')
        self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['bag'] = {str(self.product.id): 1}
        session.save()
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIn('order_form', response.context)
        self.assertIsInstance(response.context['order_form'], OrderForm)

    def test_checkout_view_get_anonymous_user(self):
        """
        Test the checkout view when the user is not authenticated.
        """
        session = self.client.session
        session['bag'] = {str(self.product.id): 1}  # Add product to bag
        session.save()

        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIn('order_form', response.context)
        self.assertIsInstance(response.context['order_form'], OrderForm)

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_view_get_no_bag(self, mock_create):
        """
        Test the GET method of the checkout view when there is no bag.
        """
        mock_create.return_value = Mock(client_secret='test_secret')
        self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['bag'] = {}
        session.save()
        response = self.client.get(reverse('checkout'))
        self.assertRedirects(response, reverse('products'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "There's nothing in your bag at the moment")

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_view_post_valid_with_sizes(self, mock_create):
        """
        Test the POST method of the checkout view with valid form data including product sizes.
        """
        mock_create.return_value = Mock(client_secret='test_secret')
        self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['bag'] = {str(self.product.id): {'items_by_size': {'M': 1}}}
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
        self.assertTrue(OrderLineItem.objects.filter(order=order, product=self.product, quantity=1).exists())

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_view_post_valid(self, mock_create):
        """
        Test the POST method of the checkout view with valid form data.
        """
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
        """
        Test the POST method of the checkout view with invalid form data.
        """
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

    @patch('checkout.views.UserProfile.objects.get')
    def test_checkout_view_get_profile_does_not_exist(self, mock_user_profile_get):
        """
        Test the GET method of the checkout view when the user profile does not exist.
        """
        mock_user_profile_get.side_effect = UserProfile.DoesNotExist

        self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['bag'] = {str(self.product.id): 1}
        session.save()
        response = self.client.get(reverse('checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)  # No messages should be generated
        self.assertIn('order_form', response.context)
        self.assertIsInstance(response.context['order_form'], OrderForm)

    def test_checkout_view_get_no_stripe_key(self):
        """
        Test the GET method of the checkout view when the stripe public key is missing.
        """
        self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['bag'] = {str(self.product.id): 1}
        session.save()

        with self.settings(STRIPE_PUBLIC_KEY=''):
            response = self.client.get(reverse('checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]).replace(' ', ''),
            'Stripe public key is missing. Did you forget to set it in your environment?'.replace(' ', '')
        )
        self.assertIn('order_form', response.context)
        self.assertIsInstance(response.context['order_form'], OrderForm)

    def test_checkout_view_post_product_does_not_exist(self):
        """
        Test the POST method of the checkout view when a product does not exist.
        """
        self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['bag'] = {str(self.product.id): 1}  # Add product to bag
        session.save()

        # Delete the product to simulate it not existing during checkout
        self.product.delete()

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

        response = self.client.post(reverse('checkout'), form_data, follow=False)

        # Check if it redirects to the 'view_bag' view
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('view_bag'))

        # Reload session
        session = self.client.session
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "One of the products in your bag wasn't found in our database. Please call us for assistance!"
        )

    @patch('checkout.views.UserProfileForm')
    def test_checkout_success_view_with_save_info(self, mock_user_profile_form):
        """
        Test the checkout success view with save_info.
        """
        self.client.login(username='testuser', password='testpass')
        session = self.client.session
        session['save_info'] = True
        session.save()

        mock_user_profile_form.return_value.is_valid.return_value = True

        response = self.client.get(reverse('checkout_success', args=[self.order.order_number]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Order successfully processed!', str(messages[0]))
        self.assertTrue(mock_user_profile_form.return_value.save.called)

    def test_checkout_success_view(self):
        """
        Test the checkout success view.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('checkout_success', args=[self.order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Order successfully processed!', str(messages[0]))

    @patch('checkout.views.stripe.PaymentIntent.modify')
    def test_cache_checkout_data_view(self, mock_modify):
        """
        Test the cache checkout data view.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('cache_checkout_data'), {
            'client_secret': 'test_pid_secret',
            'save_info': True,
        })
        self.assertEqual(response.status_code, 200)

    @patch('checkout.views.stripe.PaymentIntent.modify')
    def test_cache_checkout_data_view_exception(self, mock_modify):
        """
        Test the cache checkout data view with an exception.
        """
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
