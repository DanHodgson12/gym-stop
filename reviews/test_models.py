from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product, Category
from .models import Review
from django.core.exceptions import ValidationError


class ReviewModelTests(TestCase):

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
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            headline='Great Product',
            content='I really enjoyed this product.',
            rating=5
        )

    def test_string_representation(self):
        """Test the string representation of the Review model."""
        review_str = str(self.review)
        self.assertEqual(review_str, f"Review by testuser for Test Product")

    def test_review_creation(self):
        """Test that a review can be created and retrieved."""
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.headline, 'Great Product')
        self.assertEqual(self.review.content, 'I really enjoyed this product.')
        self.assertEqual(self.review.rating, 5)

    def test_rating_min_value(self):
        """Test that the rating cannot be less than 1."""
        self.review.rating = 0
        with self.assertRaises(ValidationError):
            self.review.full_clean()  # This will trigger the validation

    def test_rating_max_value(self):
        """Test that the rating cannot be more than 5."""
        self.review.rating = 6
        with self.assertRaises(ValidationError):
            self.review.full_clean()  # This will trigger the validation

    def test_review_without_user(self):
        """Test that a review can be created without a user (Anonymous)."""
        anonymous_review = Review.objects.create(
            product=self.product,
            user=None,
            headline='Anonymous Review',
            content='This is an anonymous review.',
            rating=4
        )
        self.assertEqual(str(anonymous_review), f"Review by Anonymous for Test Product")
        self.assertIsNone(anonymous_review.user)

