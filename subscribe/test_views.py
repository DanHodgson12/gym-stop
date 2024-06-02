from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from subscribe.models import MarketingSubscription
from subscribe.forms import MarketingSubscriptionForm, UnsubscribeForm
from unittest.mock import patch
from django.contrib import messages

class SubscribeViewsTests(TestCase):
    """
    Test cases for the subscribe views.
    """

    def setUp(self):
        """
        Set up initial data for the tests.
        """
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser', email='testuser@example.com', password='testpass'
        )

    def test_subscribe_view_get(self):
        """
        Test GET request to subscribe view.
        """
        response = self.client.get(reverse('subscribe'))
        self.assertEqual(response.status_code, 302)  # Redirect expected
        self.assertEqual(response.url, '/')

    @patch('subscribe.views.send_welcome_email')
    def test_subscribe_view_post_valid(self, mock_send_email):
        """
        Test POST request to subscribe view with valid data.
        """
        mock_send_email.return_value = True
        response = self.client.post(reverse('subscribe'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MarketingSubscription.objects.filter(email='test@example.com').exists())
        mock_send_email.assert_called_once_with('test@example.com')

    def test_subscribe_view_post_existing_user(self):
        """
        Test POST request to subscribe view with an existing user email.
        """
        self.user.userprofile.is_subscribed_to_newsletter = False
        self.user.userprofile.save()
        response = self.client.post(reverse('subscribe'), {'email': self.user.email})
        self.assertEqual(response.status_code, 302)
        self.user.userprofile.refresh_from_db()
        self.assertTrue(self.user.userprofile.is_subscribed_to_newsletter)

    def test_subscribe_view_post_existing_subscribed_user(self):
        """
        Test POST request to subscribe view with an email already subscribed.
        """
        self.user.userprofile.is_subscribed_to_newsletter = True
        self.user.userprofile.save()
        response = self.client.post(reverse('subscribe'), {'email': self.user.email})
        self.assertEqual(response.status_code, 302)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(messages_list[0]), f'The email address {self.user.email} is already subscribed to our mailing list, and is associated with an existing account.')

    def test_subscribe_view_post_invalid(self):
        """
        Test POST request to subscribe view with invalid data.
        """
        MarketingSubscription.objects.create(email='test@example.com')
        response = self.client.post(reverse('subscribe'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MarketingSubscription.objects.filter(email='test@example.com').count(), 1)

    def test_unsubscribe_view_get(self):
        """
        Test GET request to unsubscribe view.
        """
        response = self.client.get(reverse('unsubscribe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subscribe/unsubscribe.html')
        self.assertIsInstance(response.context['form'], UnsubscribeForm)

    def test_unsubscribe_view_post_valid(self):
        """
        Test POST request to unsubscribe view with valid data.
        """
        MarketingSubscription.objects.create(email='test@example.com')
        response = self.client.post(reverse('unsubscribe'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        self.assertFalse(MarketingSubscription.objects.filter(email='test@example.com').exists())

    def test_unsubscribe_view_post_valid_user(self):
        """
        Test POST request to unsubscribe view with a valid user email.
        """
        self.user.userprofile.is_subscribed_to_newsletter = True
        self.user.userprofile.save()
        response = self.client.post(reverse('unsubscribe'), {'email': self.user.email})
        self.assertEqual(response.status_code, 302)
        self.user.userprofile.refresh_from_db()
        self.assertFalse(self.user.userprofile.is_subscribed_to_newsletter)

    def test_unsubscribe_view_post_invalid(self):
        """
        Test POST request to unsubscribe view with invalid data.
        """
        response = self.client.post(reverse('unsubscribe'), {'email': 'nonexistent@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('unsubscribe'))
        self.assertFalse(MarketingSubscription.objects.filter(email='nonexistent@example.com').exists())

    @patch('subscribe.views.send_welcome_email')
    def test_send_welcome_email(self, mock_send_email):
        """
        Test that send_welcome_email is called with the correct email.
        """
        mock_send_email.return_value = True
        subscribe_url = reverse('subscribe')
        self.client.post(subscribe_url, {'email': 'newuser@example.com'})
        mock_send_email.assert_called_once_with('newuser@example.com')

    @patch('subscribe.views.os.environ.get')
    def test_send_welcome_email_with_dev_url(self, mock_environ_get):
        """
        Test send_welcome_email with DEVELOPMENT environment variable.
        """
        mock_environ_get.side_effect = lambda key, default=None: 'http://localhost:8000' if key == 'DEVELOPMENT_URL' else default
        with patch.dict('os.environ', {'DEVELOPMENT': 'True'}):
            from subscribe.views import send_welcome_email
            send_welcome_email('test@example.com')
            mock_environ_get.assert_called_with('DEVELOPMENT_URL')
