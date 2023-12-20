from django.urls import path
from app import views

urlpatterns = [
    path('api/users/', views.api_get_users, name='api_get_users'),
    path('api/user/create/', views.api_add_user, name='api_add_user'),
    path('api/user/get/', views.api_get_user, name='api_get_user'),
    path('api/user/delete/', views.api_remove_user, name='api_remove_user'),



    path('api/recipe/add/', views.api_add_recipe, name='api_add_recipe'),
    path('api/recipe/delete/', views.api_delete_recipe, name="api_delete_recipe"),
    path('api/recipe/modify/', views.api_modify_recipe, name="api_modify_recipe"),




    path('api/categories/', views.api_load_recipe_categories, name='api_load_recipe_categories'),



    
    path('api/recipe/favorites/', views.api_add_favorite, name='api_add_favorite'),
    path('api/comment/add/', views.api_add_comment, name='api_add_comment'),
    path('api/comment/delete/<int:comment_id>/', views.api_remove_comment, name='api_remove_comment'),
    path('api/comment/get/<int:recipe_id>/', views.api_get_comments, name='api_get_comments')
]
