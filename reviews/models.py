from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from products.models import Product


class Review(models.Model):
    """
    Model representing a review for a product.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    headline = models.CharField(max_length=50, blank=True)
    content = models.TextField(max_length=500, blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the review.
        """

        user = self.user.username if self.user else 'Anonymous'
        return f"Review by {user} for {self.product.name}"
