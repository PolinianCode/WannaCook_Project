from django.urls import path
from .views import *

urlpatterns = [
    path('all/', api_get_recipes, name="all_recipes"),
    path('add/', api_add_recipe, name='add_recipe'),
    path('get/', api_get_recipe, name="get_recipe"),
    path('modify/', api_modify_recipe, name='modify_recipe'),
    path('delete/', api_delete_recipe, name="delete_recipe")
]