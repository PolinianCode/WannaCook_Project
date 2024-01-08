
from django.urls import path, include
from . import views

urlpatterns = [
    path('search/', views.search_recipes, name="search_recipes")
]