from django.urls import path
from .views import *


urlpatterns = [
    path('add/', api_add_rating, name="add_rating"),
    path('delete/', api_remove_rating, name="delete_rating")
]