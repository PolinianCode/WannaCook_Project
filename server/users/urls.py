from .views import *
from django.urls import path


urlpatterns = [
    path('all/', api_get_users, name='api_get_users'),
    path('register/', api_register_user, name='api_add_user'),
    path('login/', api_login_user, name='api_get_user'),
    path('get/', api_get_user, name="api_get_user"),
    path('delete/', api_remove_user, name='api_remove_user'),
    path('modify/', api_modify_user, name="api_modify_user")
]