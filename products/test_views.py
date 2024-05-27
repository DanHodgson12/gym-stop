from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category
from django.contrib.messages import get_messages


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
