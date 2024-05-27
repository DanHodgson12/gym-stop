from django.test import TestCase
from checkout.forms import OrderForm


class OrderFormTests(TestCase):
    """
    Test cases for the OrderForm to ensure it is configured correctly.
    """

    def test_order_form_fields(self):
        """
        Test that the form includes the correct fields.
        """

        form = OrderForm()
        self.assertEqual(form.Meta.fields, (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country',
            'county',
        ))

    def test_order_form_placeholders(self):
        """
        Test that the form fields have the correct placeholders.
        """

        form = OrderForm()
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        for field_name, placeholder in placeholders.items():
            if form.fields[field_name].required:
                placeholder += ' *'
            self.assertEqual(
                form.fields[field_name].widget.attrs['placeholder'], placeholder)

    def test_order_form_autofocus(self):
        """
        Test that the 'full_name' field has autofocus set.
        """

        form = OrderForm()
        self.assertTrue(form.fields['full_name'].widget.attrs['autofocus'])

    def test_order_form_css_class(self):
        """
        Test that all form fields have the correct CSS class applied.
        """

        form = OrderForm()
        for field in form.fields:
            self.assertEqual(form.fields[field].widget.attrs['class'], 'stripe-style-input')

    def test_order_form_labels(self):
        """
        Test that all form fields have their labels removed.
        """

        form = OrderForm()
        for field in form.fields:
            self.assertFalse(form.fields[field].label)
