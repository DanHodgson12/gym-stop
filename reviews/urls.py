from django.urls import path
from . import views


app_name = 'reviews'


urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),
]