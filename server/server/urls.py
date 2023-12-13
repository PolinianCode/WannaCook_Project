from django.urls import path
from app import views

urlpatterns = [
    path('api/users/', views.api_get_users, name='api_get_users'),
    path('api/user/create/', views.api_add_user, name='api_add_user'),
    path('api/user/delete/<str:username>/', views.api_remove_user, name='api_remove_user'),
    path('api/recipe/add/', views.api_add_recipe, name='api_add_recipe'),
    path('api/recipe/delete/<int:recipe_id>/', views.api_delete_recipe, name="api_delete_recipe"),
    path('api/recipe/modify/<int:recipe_id>/', views.api_modify_recipe, name="api_modify_recipe"),
    path('api/categories/', views.api_load_recipe_categories, name='api_load_recipe_categories')
]
