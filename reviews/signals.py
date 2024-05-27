from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review


@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    """
    Update the product's average rating when a review is saved.
    """

    instance.product.update_average_rating()


@receiver(post_delete, sender=Review)
def update_product_rating_on_delete(sender, instance, **kwargs):
    """
    Update the product's average rating when a review is deleted.
    """

    instance.product.update_average_rating()
