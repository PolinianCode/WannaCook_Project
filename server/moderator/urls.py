from django.urls import path
from .views import *


urlpatterns = [
    path('add/', api_set_moderator, name="add_moderator")
]