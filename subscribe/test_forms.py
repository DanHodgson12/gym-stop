from django.test import TestCase
from subscribe.forms import MarketingSubscriptionForm, UnsubscribeForm
from subscribe.models import MarketingSubscription


class MarketingSubscriptionFormTests(TestCase):
    """
    Test cases for the MarketingSubscriptionForm.
    """

    def test_marketing_subscription_form_valid(self):
        """
        Test that the MarketingSubscriptionForm is valid with valid data.
        """

        form_data = {'email': 'test@example.com'}
        form = MarketingSubscriptionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_marketing_subscription_form_invalid(self):
        """
        Test that the MarketingSubscriptionForm is invalid with invalid data.
        """

        form_data = {'email': 'not-an-email'}
        form = MarketingSubscriptionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_marketing_subscription_form_unique_email(self):
        """
        Test that the MarketingSubscriptionForm enforces unique
        email constraint.

        Creates a MarketingSubscription object with a specific email.
        Then tries to create a form with the same email and
        checks if it's invalid.
        """

        MarketingSubscription.objects.create(email='test@example.com')
        form_data = {'email': 'test@example.com'}
        form = MarketingSubscriptionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class UnsubscribeFormTests(TestCase):
    """
    Test cases for the UnsubscribeForm.
    """

    def test_unsubscribe_form_valid(self):
        """
        Test that the UnsubscribeForm is valid with valid data.
        """

        form_data = {'email': 'test@example.com'}
        form = UnsubscribeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_unsubscribe_form_invalid(self):
        """
        Test that the UnsubscribeForm is invalid with invalid data.
        """

        form_data = {'email': 'not-an-email'}
        form = UnsubscribeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
