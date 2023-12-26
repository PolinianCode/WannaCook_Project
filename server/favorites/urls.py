from django.urls import path
from .views import *


urlpatterns = [
    path('all/', api_load_favorites, name='api_add_favorite'),
    path('add/', api_add_favorite, name='api_add_favorite'),
    path('delete/', api_remove_favorite, name='api_add_favorite'),
]