from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from categories.views import CategoriesViewSet
from comments.views import CommentsViewSet
from favorites.views import FavoritesViewSet
from ingredients.views import IngredientsViewSet, RecipeIngredientViewSet
from ratings.views import RatingsViewSet
from recipes.views import RecipesViewSet

from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'comments', CommentsViewSet, basename='comments')
router.register(r'favorites', FavoritesViewSet, basename='favorites')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'ratings', RatingsViewSet, basename='ratings')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'recipeIngredients', RecipeIngredientViewSet, basename='recipeIngredients')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/user/', include('users.urls')),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('api/data/', include('search.urls')),

    path('api/recipes/get_by_user_id/<int:user_id>/', RecipesViewSet.as_view({'get': 'get_recipes_by_user_id'}), name='get_recipes_by_user_id'),

    path('api/favorites/get_by_user_id/<int:user_id>/', FavoritesViewSet.as_view({'get': 'get_favorites_by_user_id'}), name='get_favorites_by_user_id'),
    path('api/favorites/favorite_exist_check/<int:user_id>/<int:recipe_id>/', FavoritesViewSet.as_view({'get': 'favorite_exist_check'}), name='favorite_exist_check'),
    path('api/favorites/delete_favorite/<int:user_id>/<int:recipe_id>/', FavoritesViewSet.as_view({'delete': 'delete_favorite'}), name='delete_favorite'),

    path('api/recipeingredients/delete_all_by_recipe_id/<int:recipe_id>/', RecipeIngredientViewSet.as_view({'delete': 'delete_all_by_recipe_id'}), name='delete_all_by_recipe_id'),

    path('admin/', admin.site.urls)
]
