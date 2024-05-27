from django.test import TestCase
from django.forms import Form, ImageField
from django.template import Context, Template
from django.core.files.uploadedfile import SimpleUploadedFile
from .widgets import CustomClearableFileInput
from .forms import ProductForm
from .models import Category, Product

class CustomClearableFileInputTests(TestCase):
    """
    Test cases for the CustomClearableFileInput widget to ensure it behaves correctly.
    """

    def setUp(self):
        """
        Set up test data for CustomClearableFileInput widget tests.
        """

        self.category = Category.objects.create(name='Test Category', friendly_name='Test Category')
        self.product = Product.objects.create(
            sku='12345',
            name='Test Product',
            description='Test Description',
            category=self.category,
            price=10.00,
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )

    def test_widget_template(self):
        """
        Test that the CustomClearableFileInput widget uses the correct template.
        """

        form = ProductForm(instance=self.product)
        widget = form.fields['image'].widget
        self.assertEqual(widget.template_name, 'products/custom_widget_templates/custom_clearable_file_input.html')

    def test_widget_labels(self):
        """
        Test that the CustomClearableFileInput widget has the correct labels.
        """

        form = ProductForm(instance=self.product)
        widget = form.fields['image'].widget
        self.assertEqual(widget.clear_checkbox_label, 'Remove')
        self.assertEqual(widget.initial_text, 'Current Image')
        self.assertEqual(widget.input_text, '')

    def test_widget_render(self):
        """
        Test that the CustomClearableFileInput widget renders correctly in a form.
        """

        form = ProductForm(instance=self.product)
        template = Template('{{ form.image }}')
        context = Context({'form': form})
        rendered = template.render(context)
        self.assertIn('Current Image', rendered)
        self.assertIn('Remove', rendered)
