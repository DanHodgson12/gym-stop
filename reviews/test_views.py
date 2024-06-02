from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, Category
from reviews.models import Review
from reviews.forms import ReviewForm


class ReviewViewsTests(TestCase):
    """
    Test cases for the views in the reviews app.
    """

    def setUp(self):
        """
        Set up initial data for review views tests.
        """

        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            sku='12345',
            name='Test Product',
            description='Test Description',
            category=self.category,
            price=10.00,
        )
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client.login(username='testuser', password='testpass')
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            headline='Great Product',
            content='I really enjoyed this product.',
            rating=5
        )

    def test_add_review_view_get(self):
        """
        Test GET request to add_review view.
        """

        url = reverse('reviews:add_review', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/add_review.html')
        self.assertIsInstance(response.context['form'], ReviewForm)
        self.assertEqual(response.context['product'], self.product)

    def test_add_review_view_post_valid(self):
        """
        Test POST request to add_review view with valid data.
        """

        url = reverse('reviews:add_review', args=[self.product.id])
        form_data = {
            'rating': '5',
            'headline': 'Awesome Product',
            'content': 'This is a great product!',
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse('product_detail', args=[self.product.id])
        )
        reviews = Review.objects.filter(
            product=self.product,
            user=self.user,
            headline='Awesome Product'
        )
        self.assertTrue(reviews.exists())

    def test_add_review_view_post_invalid(self):
        """
        Test POST request to add_review view with invalid data.
        """

        url = reverse('reviews:add_review', args=[self.product.id])
        form_data = {
            'rating': '',  # Missing rating
            'headline': 'Bad Product',
            'content': 'This is not a good product.',
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/add_review.html')
        self.assertFalse(
            Review.objects.filter(
                product=self.product,
                user=self.user,
                headline='Bad Product'
            ).exists()
        )

    def test_edit_review_view_get(self):
        """
        Test GET request to edit_review view.
        """

        url = reverse('reviews:edit_review', args=[self.review.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/edit_review.html')
        self.assertIsInstance(response.context['form'], ReviewForm)
        self.assertEqual(response.context['product'], self.product)
        self.assertEqual(response.context['review'], self.review)

    def test_edit_review_view_post_valid(self):
        """
        Test POST request to edit_review view with valid data.
        """

        url = reverse('reviews:edit_review', args=[self.review.id])
        form_data = {
            'rating': '4',
            'headline': 'Updated Review',
            'content': 'This product is still good, but...',
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse('product_detail', args=[self.product.id])
        )
        self.review.refresh_from_db()
        self.assertEqual(self.review.headline, 'Updated Review')
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(
            self.review.content, 'This product is still good, but...'
        )

    def test_edit_review_view_post_invalid(self):
        """
        Test POST request to edit_review view with invalid data.
        """

        url = reverse('reviews:edit_review', args=[self.review.id])
        form_data = {
            'rating': '',  # Missing rating
            'headline': 'Invalid Update',
            'content': 'This is not a valid update.',
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/edit_review.html')
        self.review.refresh_from_db()
        self.assertNotEqual(self.review.headline, 'Invalid Update')

    def test_edit_review_view_invalid_user(self):
        """
        Test that users cannot edit reviews they did not write.
        """

        User.objects.create_user(username='otheruser', password='testpass')
        self.client.login(username='otheruser', password='testpass')
        url = reverse('reviews:edit_review', args=[self.review.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse('product_detail', args=[self.product.id])
        )

    def test_delete_review_view(self):
        """
        Test POST request to delete_review view.
        """

        url = reverse('reviews:delete_review', args=[self.review.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse('product_detail', args=[self.product.id])
        )
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_delete_review_view_invalid_user(self):
        """
        Test that users cannot delete reviews they did not write.
        """

        User.objects.create_user(username='otheruser', password='testpass')
        self.client.login(username='otheruser', password='testpass')
        url = reverse('reviews:delete_review', args=[self.review.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse('product_detail', args=[self.product.id])
        )
        self.assertTrue(Review.objects.filter(id=self.review.id).exists())

    def test_delete_review_view_get_request(self):
        """
        Test GET request to delete_review view to ensure the redirect happens.
        """
        url = reverse('reviews:delete_review', args=[self.review.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse('product_detail', args=[self.product.id])
        )
