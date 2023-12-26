from django.urls import path, include
from .views import *

urlpatterns = [
    path('all/', api_get_comments, name='api_get_comments'),
    path('add/', api_add_comment, name='api_add_comment'),
    path('delete/', api_remove_comment, name='api_remove_comment'),
    path('modify/', api_modify_comment, name="api_modify_comment")
]