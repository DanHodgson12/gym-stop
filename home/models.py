from django.db import models


class MarketingSubscription(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    discount_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.email
