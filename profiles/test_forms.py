from django.test import TestCase
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from django_countries.fields import Country


class UserProfileFormTests(TestCase):

    def setUp(self):
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
        """Test that the UserProfileForm is valid with valid data."""
        form = UserProfileForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_user_profile_form_empty_data(self):
        """Test that the UserProfileForm is valid with empty data since no fields are required."""
        form = UserProfileForm(data={})
        self.assertTrue(form.is_valid())

    def test_user_profile_form_placeholders(self):
        """Test that the UserProfileForm has correct placeholders and classes."""
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
        """Test that the UserProfileForm sets autofocus on the phone number field."""
        form = UserProfileForm()
        self.assertTrue(form.fields['default_phone_number'].widget.attrs['autofocus'])
