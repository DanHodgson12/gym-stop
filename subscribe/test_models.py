from django.test import TestCase
from subscribe.models import MarketingSubscription
from django.db.utils import IntegrityError


class MarketingSubscriptionModelTests(TestCase):

    def setUp(self):
        self.subscription_email = 'test@example.com'

    def test_create_marketing_subscription(self):
        """Test that a MarketingSubscription can be created."""
        subscription = MarketingSubscription.objects.create(email=self.subscription_email)
        self.assertEqual(subscription.email, self.subscription_email)
        self.assertIsNotNone(subscription.date_subscribed)

    def test_unique_email_constraint(self):
        """Test that the email field must be unique."""
        MarketingSubscription.objects.create(email=self.subscription_email)
        with self.assertRaises(IntegrityError):
            MarketingSubscription.objects.create(email=self.subscription_email)

    def test_string_representation(self):
        """Test the string representation of the MarketingSubscription model."""
        subscription = MarketingSubscription.objects.create(email=self.subscription_email)
        self.assertEqual(str(subscription), self.subscription_email)
