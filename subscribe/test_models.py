from django.test import TestCase
from subscribe.models import MarketingSubscription
from django.db.utils import IntegrityError


class MarketingSubscriptionModelTests(TestCase):
    """
    Test cases for the MarketingSubscription model.
    """

    def setUp(self):
        """
        Set up initial data for the tests.
        """

        self.subscription_email = 'test@example.com'

    def test_create_marketing_subscription(self):
        """
        Test that a MarketingSubscription can be created.

        Creates a MarketingSubscription object and checks if it's
        created successfully.
        """

        subscription = MarketingSubscription.objects.create(
            email=self.subscription_email
        )
        self.assertEqual(subscription.email, self.subscription_email)
        self.assertIsNotNone(subscription.date_subscribed)

    def test_unique_email_constraint(self):
        """
        Test that the email field must be unique.

        Creates a MarketingSubscription object with a specific email.
        Then tries to create another object with the same email and
        checks if it raises IntegrityError.
        """

        MarketingSubscription.objects.create(email=self.subscription_email)
        with self.assertRaises(IntegrityError):
            MarketingSubscription.objects.create(email=self.subscription_email)

    def test_string_representation(self):
        """
        Test the string representation of the MarketingSubscription model.

        Creates a MarketingSubscription object and checks its
        string representation.
        """

        email = self.subscription_email
        subscription = MarketingSubscription.objects.create(email=email)
        self.assertEqual(str(subscription), self.subscription_email)
