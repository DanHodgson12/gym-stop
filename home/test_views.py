from django.test import TestCase
from django.urls import reverse


class HomeViewsTests(TestCase):
    def test_index_view(self):
        """Test that the index view returns a 200 status code and uses the correct template."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_privacy_policy_view(self):
        """Test that the privacy policy view returns a 200 status code and uses the correct template."""
        response = self.client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/privacy_policy.html')

    def test_terms_and_conditions_view(self):
        """Test that the terms and conditions view returns a 200 status code and uses the correct template."""
        response = self.client.get(reverse('terms_and_conditions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/terms_and_conditions.html')

    def test_returns_policy_view(self):
        """Test that the returns policy view returns a 200 status code and uses the correct template."""
        response = self.client.get(reverse('returns_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/returns_policy.html')

    def test_page_not_found_view(self):
        """Test that the page not found view returns a 404 status code and uses the correct template."""
        response = self.client.get('/non-existent-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'home/404.html')
