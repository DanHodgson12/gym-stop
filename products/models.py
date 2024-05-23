from django.db import models
from django.db.models import Avg
from django.core.validators import MaxValueValidator


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, blank=True, default=0,
        validators=[MaxValueValidator(5)])
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def update_average_rating(self):
        average = self.reviews.aggregate(Avg('rating'))['rating__avg']
        self.rating = average or 0  # Assign 0 if there are no ratings
        self.save()

    def rating_percentage(self):
        if self.rating is not None:
            return self.rating * 20  # Convert rating (out of 5) to percentage (out of 100)
        return 0  # Return 0 if there is no rating

    def __str__(self):
        return self.name
