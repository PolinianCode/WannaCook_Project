from django.urls import path, include

urlpatterns = [

    path('api/user/', include('users.urls')),
    path('api/recipe/', include('recipes.urls')),
    path('api/category/', include('categories.urls')),
    path('api/rating/', include('rating.urls')),
    path('api/recipes/', include('search.urls')),
    path('api/ingredients/', include('ingredient.urls')),
    path('api/favorites/', include('favorites.urls')),
    path('api/comment/', include('comments.urls')),
    path('api/moderator/', include('moderator.urls'))
]
