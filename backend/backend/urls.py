from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from categories.views import CategoriesViewSet

router = DefaultRouter()
router.register(r'categories', CategoriesViewSet, basename='categories')


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
