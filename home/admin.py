from django.contrib import admin
from .models import MarketingSubscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'date_subscribed',
    )

    ordering = ('-date_subscribed',)

admin.site.register(MarketingSubscription, SubscriptionAdmin)
