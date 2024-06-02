from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import UserProfile
from checkout.models import Order
from products.models import Product
from unittest.mock import patch
import json
import stripe
import uuid


class WebhookTests(TestCase):
    """
    Test cases for the Stripe webhook handler.
    """

    def setUp(self):
        """
        Set up the initial data for the webhook tests.
        """

        self.client = Client()
        self.url = reverse('webhook')
        self.user, created = User.objects.get_or_create(
            username='testuser', password='password'
        )
        self.user_profile, created = UserProfile.objects.get_or_create(
            user=self.user
        )

        # Creating a test product
        self.product = Product.objects.create(
            name="Test Product",
            price=10.00,
        )

        self.payment_intent_id = f"pi_{uuid.uuid4().hex[:24]}"
        self.charge_id = f"ch_{uuid.uuid4().hex[:24]}"
        self.payload = {
            'id': 'evt_test_webhook',
            'object': 'event',
            'type': 'payment_intent.succeeded',
            'data': {
                'object': {
                    'id': self.payment_intent_id,
                    'object': 'payment_intent',
                    'amount_received': 2000,
                    'currency': 'usd',
                    'payment_method_types': ['card'],
                    'metadata': {
                        'bag': json.dumps({str(self.product.id): 2}),
                        'save_info': 'True',
                        'username': 'testuser'
                    },
                    'latest_charge': self.charge_id,
                    'shipping': {
                        'name': 'Test User',
                        'address': {
                            'line1': '123 Test St',
                            'line2': '',
                            'city': 'Test City',
                            'postal_code': '12345',
                            'country': 'US',
                            'state': 'Test State'
                        },
                        'phone': '123-456-7890'
                    }
                }
            }
        }
        self.sig_header = 't=1600000000,v1=fake_signature,v0=fake_signature'

    @patch('stripe.Charge.retrieve')
    @patch('stripe.Webhook.construct_event')
    def test_webhook_valid_event(
        self, mock_construct_event, mock_retrieve_charge
    ):
        """
        Test handling of a valid webhook event.
        """

        mock_construct_event.return_value = stripe.Event.construct_from(
            self.payload, stripe.api_key
        )

        mock_retrieve_charge.return_value = stripe.Charge.construct_from({
            'id': self.charge_id,
            'amount': 2000,
            'currency': 'usd',
            'billing_details': {
                'name': 'Test User',
                'email': 'test@example.com'
            }
        }, stripe.api_key)

        response = self.client.post(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE=self.sig_header
        )

        self.assertEqual(response.status_code, 200)

        # Verify the order was created
        self.assertTrue(
            Order.objects.filter(stripe_pid=self.payment_intent_id).exists()
        )

    @patch(
        'stripe.Webhook.construct_event',
        side_effect=stripe.error.SignatureVerificationError(
            'Invalid signature', 'sig'
        )
    )
    def test_webhook_invalid_signature(self, mock_construct_event):
        """
        Test handling of a webhook event with an invalid signature.
        """

        response = self.client.post(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE=self.sig_header
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid signature', response.content.decode())

    @patch(
        'stripe.Webhook.construct_event',
        side_effect=ValueError('Invalid payload')
    )
    def test_webhook_invalid_payload(self, mock_construct_event):
        """
        Test handling of a webhook event with an invalid payload.
        """

        response = self.client.post(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE=self.sig_header
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload', response.content.decode())

    @patch(
        'stripe.Webhook.construct_event',
        side_effect=Exception('Unexpected error')
    )
    def test_webhook_unexpected_error(self, mock_construct_event):
        """
        Test handling of a webhook event with an unexpected error.
        """

        response = self.client.post(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE=self.sig_header
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('Unexpected error', response.content.decode())
