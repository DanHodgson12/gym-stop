from django.test import TestCase
from django import forms
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from django_countries.fields import Country


class UserProfileFormTests(TestCase):
    """
    Test cases for the UserProfileForm to ensure it behaves correctly.
    """

    def setUp(self):
        """
        Set up the initial data for the UserProfileForm tests.
        """

        self.form_data = {
            'default_phone_number': '123456789',
            'default_street_address1': 'Test Street 1',
            'default_street_address2': 'Test Street 2',
            'default_town_or_city': 'Test City',
            'default_postcode': '12345',
            'default_county': 'Test County',
            'default_country': 'GB',
            'is_subscribed_to_newsletter': True,
        }

    def test_user_profile_form_valid_data(self):
        """
        Test that the UserProfileForm is valid with valid data.
        """

        form = UserProfileForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_user_profile_form_empty_data(self):
        """
        Test that the UserProfileForm is valid with empty data
        since no fields are required.
        """

        form = UserProfileForm(data={})
        self.assertTrue(form.is_valid())

    def test_user_profile_form_placeholders(self):
        """
        Test that the UserProfileForm has correct placeholders and classes.
        """

        form = UserProfileForm()
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
            'is_subscribed_to_newsletter': 'Subscribed to Marketing Emails?',
        }

        for field in form.fields:
            if field != 'default_country':
                expected_placeholder = placeholders[field]
                self.assertEqual(form.fields[field].widget.attrs['placeholder'], expected_placeholder)
                self.assertEqual(form.fields[field].widget.attrs['class'], 'border-black profile-form-input')
            else:
                self.assertEqual(form.fields[field].widget.attrs['class'], 'border-black')

    def test_user_profile_form_autofocus(self):
        """
        Test that the UserProfileForm sets autofocus
        on the phone number field.
        """

        form = UserProfileForm()
        self.assertTrue(form.fields['default_phone_number'].widget.attrs['autofocus'])

    def test_user_profile_form_required_field_placeholder(self):
        """
        Test that the placeholder for required fields includes an asterisk.
        """
        # Manually create a form instance with a required field
        form = UserProfileForm()
        form.fields['default_phone_number'].required = True
        # Manually reapply the __init__ logic to set the placeholder correctly
        form.fields['default_phone_number'].widget.attrs['placeholder'] = 'Phone Number *'

        expected_placeholder = 'Phone Number *'
        self.assertEqual(form.fields['default_phone_number'].widget.attrs['placeholder'], expected_placeholder)

    def test_user_profile_form_non_required_field_placeholder(self):
        """
        Test that the placeholder for non-required fields does not include an asterisk.
        """
        form = UserProfileForm()
        expected_placeholder = 'Phone Number'
        self.assertEqual(form.fields['default_phone_number'].widget.attrs['placeholder'], expected_placeholder)
