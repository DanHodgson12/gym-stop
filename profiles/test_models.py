from django.test import TestCase
from django.contrib.auth.models import User
from django_countries.fields import Country
from profiles.models import UserProfile


class UserProfileModelTests(TestCase):
    """
    Test cases for the UserProfile model to ensure it behaves correctly.
    """

    def setUp(self):
        """
        Set up a user for testing.
        """

        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_user_profile_created_on_user_creation(self):
        """
        Test that a UserProfile is created when a User is created.
        """

        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.user.username, 'testuser')

    def test_user_profile_updated_on_user_update(self):
        """
        Test that a UserProfile is updated when a User is updated.
        """

        self.user.username = 'updateduser'
        self.user.save()
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.user.username, 'updateduser')

    def test_user_profile_str_method(self):
        """
        Test the __str__ method of UserProfile.
        """

        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(str(profile), 'testuser')

    def test_user_profile_fields(self):
        """
        Test the fields of the UserProfile.
        """

        profile = UserProfile.objects.get(user=self.user)
        profile.default_phone_number = '123456789'
        profile.default_street_address1 = 'Test Street 1'
        profile.default_street_address2 = 'Test Street 2'
        profile.default_town_or_city = 'Test City'
        profile.default_postcode = '12345'
        profile.default_county = 'Test County'
        profile.default_country = Country(code='GB')
        profile.is_subscribed_to_newsletter = True
        profile.save()

        self.assertEqual(profile.default_phone_number, '123456789')
        self.assertEqual(profile.default_street_address1, 'Test Street 1')
        self.assertEqual(profile.default_street_address2, 'Test Street 2')
        self.assertEqual(profile.default_town_or_city, 'Test City')
        self.assertEqual(profile.default_postcode, '12345')
        self.assertEqual(profile.default_county, 'Test County')
        self.assertEqual(profile.default_country, Country(code='GB'))
        self.assertTrue(profile.is_subscribed_to_newsletter)
