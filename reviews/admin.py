from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'rating',
        'user',
        'headline',
        'created_at',
    )

    ordering = ('created_at',)


admin.site.register(Review, ReviewAdmin)
