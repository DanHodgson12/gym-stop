from django.db import models
from django.db.models import Avg
from django.core.validators import MaxValueValidator


class Category(models.Model):
    """
    Represents a product's category.
    """

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        """
        String representation of the category, returning its name.
        """

        return self.name

    def get_friendly_name(self):
        """
        Returns the friendly name of the category.
        """

        return self.friendly_name


class Product(models.Model):
    """
    Represents a product available in the store.
    """

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
        """
        Update the product's average rating based on its reviews.
        """

        average = self.reviews.aggregate(Avg('rating'))['rating__avg']
        self.rating = average or 0
        self.save()

    def rating_percentage(self):
        """
        Convert the product's rating to a percentage.
        """

        if self.rating is not None:
            return self.rating * 20
        return 0

    def __str__(self):
        """
        String representation of the product, returning its name.
        """

        return self.name
