
from django.urls import path
from .views import *

urlpatterns = [
    path('search/', api_search_recipes, name="search_recipe")
]
