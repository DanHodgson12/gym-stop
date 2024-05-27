from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product, Category
from reviews.models import Review


class ReviewSignalsTests(TestCase):
    """
    Test cases for the signals related to the Review model to ensure they behave correctly.
    """

    def setUp(self):
        """
        Set up initial data for Review signal tests.
        """

        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            sku='12345',
            name='Test Product',
            description='Test Description',
            category=self.category,
            price=10.00,
        )
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_update_product_rating_on_review_save(self):
        """
        Test that the product rating is updated when a review is saved.
        """

        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            headline='Great Product',
            content='I really enjoyed this product.'
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.rating, 5.0)

    def test_update_product_rating_on_review_delete(self):
        """
        Test that the product rating is updated when a review is deleted.
        """

        review1 = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            headline='Great Product',
            content='I really enjoyed this product.'
        )
        review2 = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=3,
            headline='Okay Product',
            content='This product was okay.'
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.rating, 4.0)

        review1.delete()
        self.product.refresh_from_db()
        self.assertEqual(self.product.rating, 3.0)

        review2.delete()
        self.product.refresh_from_db()
        self.assertEqual(self.product.rating, 0)
