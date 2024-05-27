from django.test import TestCase
from checkout.forms import OrderForm


class OrderFormTests(TestCase):

    def test_order_form_fields(self):
        form = OrderForm()
        self.assertEqual(form.Meta.fields, (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country',
            'county',
        ))

    def test_order_form_placeholders(self):
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
        form = OrderForm()
        self.assertTrue(form.fields['full_name'].widget.attrs['autofocus'])

    def test_order_form_css_class(self):
        form = OrderForm()
        for field in form.fields:
            self.assertEqual(form.fields[field].widget.attrs['class'], 'stripe-style-input')

    def test_order_form_labels(self):
        form = OrderForm()
        for field in form.fields:
            self.assertFalse(form.fields[field].label)
