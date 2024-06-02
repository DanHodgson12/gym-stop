from django.test import TestCase
from django.core.validators import ValidationError
from django.contrib.auth.models import User
from .models import Category, Product
from reviews.models import Review
from django.db.models import Avg


class CategoryModelTests(TestCase):
    """
    Test cases for the Category model to ensure it behaves correctly.
    """

    def setUp(self):
        """
        Set up the initial data for the Category model tests.
        """

        self.category = Category.objects.create(
            name='Test Category',
            friendly_name='Friendly Test Category'
        )

    def test_category_str_method(self):
        """
        Test the __str__ method of the Category model.
        """

        self.assertEqual(str(self.category), 'Test Category')

    def test_get_friendly_name(self):
        """
        Test the get_friendly_name method of the Category model.
        """

        self.assertEqual(self.category.get_friendly_name(), 'Friendly Test Category')


class ProductModelTests(TestCase):
    """
    Test cases for the Product model to ensure it behaves correctly.
    """

    def setUp(self):
        """
        Set up the initial data for the Product model tests.
        """

        self.category = Category.objects.create(
            name='Test Category'
        )
        self.product = Product.objects.create(
            sku='12345',
            name='Test Product',
            description='Test Description',
            category=self.category,
            price=19.99,
            has_sizes=True,
            rating=4.5,
            image_url='http://example.com/image.jpg',
            image=None
        )
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_product_str_method(self):
        """
        Test the __str__ method of the Product model.
        """

        self.assertEqual(str(self.product), 'Test Product')

    def test_update_average_rating_no_reviews(self):
        """
        Test the update_average_rating method of the Product model with no reviews.
        """

        self.product.update_average_rating()
        self.assertEqual(self.product.rating, 0)

    def test_update_average_rating_with_reviews(self):
        """
        Test the update_average_rating method of the Product model with reviews.
        """

        Review.objects.create(
            product=self.product,
            user=self.user,
            headline='Great Product',
            content='I really enjoyed this product.',
            rating=5
        )
        Review.objects.create(
            product=self.product,
            user=self.user,
            headline='Not bad',
            content='The product was okay.',
            rating=3
        )
        self.product.update_average_rating()
        expected_rating = self.product.reviews.aggregate(Avg('rating'))['rating__avg']
        self.assertEqual(self.product.rating, expected_rating)

    def test_rating_percentage(self):
        """
        Test the rating_percentage method of the Product model.
        """

        self.product.rating = 4.5
        self.assertEqual(self.product.rating_percentage(), 90)

    def test_rating_percentage_none(self):
        """
        Test the rating_percentage method of the Product model when rating is None.
        """

        self.product.rating = None
        self.assertEqual(self.product.rating_percentage(), 0)

    def test_max_value_validator_for_rating(self):
        """
        Test that the rating field respects the MaxValueValidator.
        """

        with self.assertRaises(ValidationError):
            self.product.rating = 6
            self.product.full_clean()
