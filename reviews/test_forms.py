from django.test import TestCase
from django.utils.safestring import SafeData
from .forms import ReviewForm
from .models import Review
from products.models import Product, Category
from django.contrib.auth.models import User


class ReviewFormTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            sku='12345',
            name='Test Product',
            description='Test Description',
            category=self.category,
            price=10.00,
        )
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_rating_choices(self):
        """Test that the rating choices are correctly set."""
        form = ReviewForm()
        expected_choices = [
            (1, '<i class="fa fa-star filled-star"></i>'),
            (2, '<i class="fa fa-star filled-star"></i>' +
                '<i class="fa fa-star filled-star"></i>'),
            (3, '<i class="fa fa-star filled-star"></i>' +
                '<i class="fa fa-star filled-star"></i>' +
                '<i class="fa fa-star filled-star"></i>'),
            (4, '<i class="fa fa-star filled-star"></i>' +
                '<i class="fa fa-star filled-star"></i>' +
                '<i class="fa fa-star filled-star"></i>' +
                '<i class="fa fa-star filled-star"></i>'),
            (5, '<i class="fa fa-star filled-star"></i>' +
                '<i class="fa fa-star filled-star"></i>' +
                '<i class="fa fa-star filled-star"></i>' +
                '<i class="fa fa-star filled-star"></i>' +
                '<i class="fa fa-star filled-star"></i>')
        ]
        self.assertEqual(form.fields['rating'].choices, expected_choices)

    def test_custom_labels(self):
        """Test that the custom labels are set correctly."""
        form = ReviewForm()
        self.assertTrue(isinstance(form.fields['headline'].label, SafeData))
        self.assertTrue(isinstance(form.fields['content'].label, SafeData))
        self.assertIn("Headline <span class='text-muted'>(optional)</span>", form.fields['headline'].label)
        self.assertIn("Content <span class='text-muted'>(optional)</span>", form.fields['content'].label)

    def test_custom_placeholders(self):
        """Test that the custom placeholders are set correctly."""
        form = ReviewForm()
        self.assertEqual(form.fields['headline'].widget.attrs['placeholder'], 'Brief headline for your review')
        self.assertEqual(form.fields['content'].widget.attrs['placeholder'], 'Write your review here')

    def test_valid_form(self):
        """Test that the form is valid with all required fields."""
        form_data = {
            'rating': '5',
            'headline': 'Great Product',
            'content': 'I really enjoyed this product.'
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_no_rating(self):
        """Test that the form is invalid if no rating is provided."""
        form_data = {
            'headline': 'Great Product',
            'content': 'I really enjoyed this product.'
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
