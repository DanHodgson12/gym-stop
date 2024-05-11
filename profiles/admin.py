from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'default_phone_number',
            'default_street_address1', 'default_street_address2',
            'default_town_or_city', 'default_county',
            'default_country', 'default_postcode',
            'is_subscribed_to_newsletter')

    list_display = ('user', 'default_phone_number',
                    'is_subscribed_to_newsletter')

    ordering = ('-user',)


admin.site.register(UserProfile, UserProfileAdmin)
