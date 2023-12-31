from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from categories.views import CategoriesViewSet
from comments.views import CommentsViewSet
from favorites.views import FavoritesViewSet
from ingredients.views import IngredientsViewSet
from ratings.views import RatingsViewSet
from recipes.views import RecipesViewSet



router = DefaultRouter()
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'comments', CommentsViewSet, basename='comments')
router.register(r'favorites', FavoritesViewSet, basename='favorites')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'ratings', RatingsViewSet, basename='ratings')
router.register(r'recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('api/', include(router.urls)),

    # path('api/comments/', include('comments.urls')),
    # path('api/favorites/', include('favorites.urls')),
    # path('api/ingredients/', include('ingredients.urls')),
    # path('api/ratings/', include('ratings.urls')),
    # path('api/recipes/', include('recipes.urls')),
    # path('api/user/', include('users.urls')),

    path('api/user/', include('users.urls')),
    path('api/recipes/', include('search.urls')),
    path('admin/', admin.site.urls)
]
