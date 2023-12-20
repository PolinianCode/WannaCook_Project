from django.urls import path
from app import views

urlpatterns = [
    #USERS
    path('api/users/', views.api_get_users, name='api_get_users'),
    path('api/user/create/', views.api_add_user, name='api_add_user'),
    path('api/user/get/', views.api_get_user, name='api_get_user'),
    path('api/user/delete/', views.api_remove_user, name='api_remove_user'),


    #RECIPE
    path('api/recipe/add/', views.api_add_recipe, name='api_add_recipe'),
    path('api/recipe/get/', views.api_get_recipe, name='api_get_recipe'),
    path('api/recipe/modify/', views.api_modify_recipe, name="api_modify_recipe"),
    path('api/recipe/delete/', views.api_delete_recipe, name="api_delete_recipe"),


    #CATEGORIES
    path('api/categories/', views.api_load_recipe_categories, name='api_load_recipe_categories'),
    path('api/category/add/', views.api_add_category, name='api_add_category'),
    path('api/category/delete/', views.api_delete_category, name='api_delete_category'),

    #INGREDIENTS
    path('api/ingredients/', views.api_load_recipe_ingredients, name='api_load_recipe_ingredients'),
    path('api/ingredient/add/', views.api_add_ingredient, name='api_add_ingredient'),
    path('api/ingredient/delete/', views.api_delete_ingredient, name='api_delete_ingredient'),

    #SEARCH
    path('api/recipe/search/', views.api_search_recipes, name='api_search_recipes'),


    #FAVORITES
    path('api/recipe/favorites/', views.api_load_favorites, name='api_add_favorite'),
    path('api/recipe/favorite/add/', views.api_add_favorite, name='api_add_favorite'),
    path('api/recipe/favorite/delete/', views.api_remove_favorite, name='api_add_favorite'),


    #COMMENTS
    path('api/recipe/comments/', views.api_get_comments, name='api_get_comments'),
    path('api/recipe/comment/add/', views.api_add_comment, name='api_add_comment'),
    path('api/recipe/comment/delete/', views.api_remove_comment, name='api_remove_comment'),
    path('api/recipe/comment/modify/', views.api_modify_comment, name="api_modify_comment"),




    #Moderator
    path('api/moderator/add/', views.api_set_moderator, name="api_set_moderator")
]
