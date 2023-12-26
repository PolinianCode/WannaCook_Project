from django.urls import path
from .views import *


urlpatterns = [
    path('add/', api_add_ingredient, name="add_ingredient"),
    path('delete/', api_delete_ingredient, name="delete_ingredient"),
    path('all/', api_load_recipe_ingredients, name="get_all_ingredients")
]