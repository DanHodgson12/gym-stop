from django.db import models


class MarketingSubscription(models.Model):
    """
    Model representing a subscription to marketing emails.
    """

    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the MarketingSubscription.
        """

        return self.email
