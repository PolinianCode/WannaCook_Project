
from django.urls import path, include
from .views import register_user, login_user, logout_user, token_check

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('token_check/', token_check, name='token_check')
]