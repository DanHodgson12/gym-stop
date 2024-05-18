from django.contrib import admin
from .models import Product, Category
from reviews.models import Review


class ReviewInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = Review
    extra = 0  # Number of empty review forms to display


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)
    inlines = [ReviewInline]  # Include the ReviewInline in the Product admin page


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
