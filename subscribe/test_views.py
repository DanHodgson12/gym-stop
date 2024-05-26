from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from subscribe.models import MarketingSubscription
from subscribe.forms import MarketingSubscriptionForm, UnsubscribeForm
from unittest.mock import patch


class SubscribeViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser', email='testuser@example.com', password='testpass'
        )

    def test_subscribe_view_get(self):
        """Test GET request to subscribe view."""
        response = self.client.get(reverse('subscribe'))
        self.assertEqual(response.status_code, 302)  # Redirect expected
        self.assertEqual(response.url, '/')

    @patch('subscribe.views.send_welcome_email')
    def test_subscribe_view_post_valid(self, mock_send_email):
        """Test POST request to subscribe view with valid data."""
        mock_send_email.return_value = True
        response = self.client.post(reverse('subscribe'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MarketingSubscription.objects.filter(email='test@example.com').exists())
        mock_send_email.assert_called_once_with('test@example.com')

    def test_subscribe_view_post_invalid(self):
        """Test POST request to subscribe view with invalid data."""
        MarketingSubscription.objects.create(email='test@example.com')
        response = self.client.post(reverse('subscribe'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MarketingSubscription.objects.filter(email='test@example.com').count(), 1)

    def test_unsubscribe_view_get(self):
        """Test GET request to unsubscribe view."""
        response = self.client.get(reverse('unsubscribe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subscribe/unsubscribe.html')
        self.assertIsInstance(response.context['form'], UnsubscribeForm)

    def test_unsubscribe_view_post_valid(self):
        """Test POST request to unsubscribe view with valid data."""
        MarketingSubscription.objects.create(email='test@example.com')
        response = self.client.post(reverse('unsubscribe'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        self.assertFalse(MarketingSubscription.objects.filter(email='test@example.com').exists())

    def test_unsubscribe_view_post_invalid(self):
        """Test POST request to unsubscribe view with invalid data."""
        response = self.client.post(reverse('unsubscribe'), {'email': 'nonexistent@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('unsubscribe'))
        self.assertFalse(MarketingSubscription.objects.filter(email='nonexistent@example.com').exists())
