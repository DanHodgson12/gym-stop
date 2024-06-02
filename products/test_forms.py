from django.test import TestCase
from .forms import ProductForm
from .models import Category
from .widgets import CustomClearableFileInput


class ProductFormTests(TestCase):
    """
    Test cases for the ProductForm to ensure it behaves correctly.
    """

    def setUp(self):
        """
        Set up the initial data for the ProductForm tests.
        """

        self.category = Category.objects.create(
            name='Test Category', friendly_name='Friendly Test Category'
        )
        self.form_data = {
            'sku': '12345',
            'name': 'Test Product',
            'description': 'Test Description',
            'category': self.category.id,
            'price': 19.99,
            'has_sizes': True,
            'image_url': 'http://example.com/image.jpg',
            'image': None
        }

    def test_product_form_valid_data(self):
        """
        Test that the ProductForm is valid with valid data.
        """

        form = ProductForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_product_form_empty_data(self):
        """
        Test that the ProductForm is invalid with empty data.
        """

        form = ProductForm(data={})
        self.assertFalse(form.is_valid())

    def test_product_form_excluded_fields(self):
        """
        Test that the ProductForm does not include the rating field.
        """

        form = ProductForm(data=self.form_data)
        self.assertNotIn('rating', form.fields)

    def test_product_form_custom_widget(self):
        """
        Test that the ProductForm uses the CustomClearableFileInput widget for the image field.
        """

        form = ProductForm()
        self.assertIsInstance(form.fields['image'].widget, CustomClearableFileInput)

    def test_product_form_field_classes(self):
        """
        Test that the ProductForm fields have the correct CSS class.
        """

        form = ProductForm()
        for field_name, field in form.fields.items():
            self.assertEqual(field.widget.attrs['class'], 'border-black')

    def test_product_form_category_choices(self):
        """
        Test that the ProductForm category field choices are correctly set.
        """

        form = ProductForm()
        self.assertEqual(
            form.fields['category'].choices,
            [(self.category.id, self.category.get_friendly_name())]
        )
