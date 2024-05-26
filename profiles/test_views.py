from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from profiles.models import UserProfile
from checkout.models import Order
from django_countries.fields import Country


class ProfileViewsTests(TestCase):

    def setUp(self):
        """Set up a user and user profile for testing."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.client.login(username='testuser', password='testpass')

    def test_profile_view_get(self):
        """Test that the profile view returns a 200 status code and uses the correct template."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertIn('form', response.context)
        self.assertIn('orders', response.context)

    def test_profile_view_post_valid_data(self):
        """Test that the profile view updates the profile with valid data."""
        response = self.client.post(reverse('profile'), {
            'default_phone_number': '123456789',
            'default_street_address1': 'Test Street 1',
            'default_street_address2': 'Test Street 2',
            'default_town_or_city': 'Test City',
            'default_postcode': '12345',
            'default_county': 'Test County',
            'default_country': 'GB',
            'is_subscribed_to_newsletter': True,
        })
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.default_phone_number, '123456789')
        self.assertEqual(self.profile.default_street_address1, 'Test Street 1')
        self.assertEqual(self.profile.default_street_address2, 'Test Street 2')
        self.assertEqual(self.profile.default_town_or_city, 'Test City')
        self.assertEqual(self.profile.default_postcode, '12345')
        self.assertEqual(self.profile.default_county, 'Test County')
        self.assertEqual(self.profile.default_country, Country(code='GB'))
        self.assertTrue(self.profile.is_subscribed_to_newsletter)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Profile updated successfully')

    def test_order_history_view(self):
        """Test that the order history view returns a 200 status code and uses the correct template."""
        order = Order.objects.create(order_number='12345', user_profile=self.profile)
        response = self.client.get(reverse('order_history', args=[order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertEqual(response.context['order'], order)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), (
            f'This is a past confirmation for order number {order.order_number}. '
            'A confirmation email was sent on the order date.'
        ))
