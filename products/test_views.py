from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category
from django.contrib.messages import get_messages
from checkout.models import Order
from profiles.models import UserProfile
from reviews.forms import ReviewForm


class ProductsViewsTests(TestCase):
    """
    Test cases for the views in the products app.
    """

    def setUp(self):
        """
        Set up test data for products views.
        """

        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.superuser = User.objects.create_superuser(username='admin', password='adminpass')
        self.category = Category.objects.create(name='Test Category', friendly_name='Test Category')
        self.product = Product.objects.create(
            sku='12345',
            name='Test Product',
            description='Test Description',
            category=self.category,
            price=10.00
        )

    def test_all_products_view(self):
        """
        Test the all_products view.
        """

        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, 'Test Product')

    def test_product_detail_view(self):
        """
        Test the product_detail view.
        """

        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertContains(response, 'Test Product')

    def test_product_detail_view_with_purchased_product(self):
        """
        Test the product_detail view where the user has purchased the product.
        """
        # Create a user profile and an order for the product
        profile = UserProfile.objects.get(user=self.user)
        order = Order.objects.create(user_profile=profile)
        order.lineitems.create(product=self.product, quantity=1)

        self.client.login(username='testuser', password='testpass')

        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertContains(response, 'Test Product')
        self.assertIn('review_form', response.context)
        self.assertIsInstance(response.context['review_form'], ReviewForm)

    def test_add_product_view_not_superuser(self):
        """
        Test the add_product view as a non-superuser.
        """

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        response = self.client.post(reverse('add_product'), {})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_add_product_view_superuser(self):
        """
        Test the add_product view as a superuser.
        """

        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')
        form_data = {
            'sku': '54321',
            'name': 'New Product',
            'description': 'New Description',
            'category': self.category.id,
            'price': 20.00,
        }
        response = self.client.post(reverse('add_product'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('product_detail', args=[Product.objects.get(name='New Product').id]))

    def test_add_product_view_superuser_invalid_data(self):
        """
        Test the add_product view with invalid form data as a superuser.
        """

        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('add_product'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Failed to add product. Please ensure the form is valid.')

    def test_edit_product_view_not_superuser(self):
        """
        Test the edit_product view as a non-superuser.
        """

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('edit_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        response = self.client.post(reverse('edit_product', args=[self.product.id]), {})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_edit_product_view_superuser(self):
        """
        Test the edit_product view as a superuser.
        """

        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('edit_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/edit_product.html')
        form_data = {
            'sku': '67890',
            'name': 'Updated Product',
            'description': 'Updated Description',
            'category': self.category.id,
            'price': 30.00,
        }
        response = self.client.post(reverse('edit_product', args=[self.product.id]), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('product_detail', args=[self.product.id]))
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_edit_product_view_superuser_invalid_data(self):
        """
        Test the edit_product view with invalid form data as a superuser.
        """

        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('edit_product', args=[self.product.id]), {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/edit_product.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Failed to update product. Please ensure the form is valid.')

    def test_delete_product_view_not_superuser(self):
        """
        Test the delete_product view as a non-superuser.
        """

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('delete_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_delete_product_view_superuser(self):
        """
        Test the delete_product view as a superuser.
        """

        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('delete_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('products'))
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_delete_product_view_superuser_invalid_product(self):
        """
        Test the delete_product view as a superuser with an invalid product id.
        """

        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('delete_product', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_all_products_view_no_results(self):
        """
        Test the all_products view with no search results.
        """

        response = self.client.get(reverse('products') + '?q=NonExistentProduct')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "No products found")

    def test_all_products_view_sorting(self):
        """
        Test the all_products view with sorting.
        """
        response = self.client.get(reverse('products') + '?sort=name&direction=asc')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, 'Test Product')
        self.assertIn('current_sorting', response.context)
        self.assertEqual(response.context['current_sorting'], 'name_asc')

    def test_all_products_view_category_filtering(self):
        """
        Test the all_products view with category filtering.
        """
        response = self.client.get(reverse('products') + f'?category={self.category.name}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, 'Test Product')
        self.assertIn('current_categories', response.context)
        self.assertEqual(len(response.context['current_categories']), 1)
        self.assertEqual(response.context['current_categories'][0], self.category)

    def test_all_products_view_search(self):
        """
        Test the all_products view with search query.
        """
        response = self.client.get(reverse('products') + '?q=Test+Product')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, 'Test Product')
        self.assertIn('search_term', response.context)
        self.assertEqual(response.context['search_term'], 'Test Product')

    def test_all_products_view_empty_search(self):
        """
        Test the all_products view with empty search query.
        """
        response = self.client.get(reverse('products') + '?q=')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('products'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "You didn't enter any search criteria!")

    def test_all_products_view_sorting_by_category(self):
        """
        Test the all_products view with sorting by category.
        """
        response = self.client.get(reverse('products') + '?sort=category&direction=asc')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, 'Test Product')
        self.assertIn('current_sorting', response.context)
        self.assertEqual(response.context['current_sorting'], 'category_asc')

    def test_all_products_view_sorting_desc(self):
        """
        Test the all_products view with descending sorting direction.
        """
        response = self.client.get(reverse('products') + '?sort=name&direction=desc')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, 'Test Product')
        self.assertIn('current_sorting', response.context)
        self.assertEqual(response.context['current_sorting'], 'name_desc')
