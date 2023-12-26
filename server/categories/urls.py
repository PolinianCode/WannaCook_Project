from django.urls import path
from .views import *

urlpatterns = [
    path('all/', api_load_recipe_categories, name='all_categories'),
    path('add/', api_add_category, name="add_category"),
    path('delete/', api_delete_category, name="delete_category")
]
