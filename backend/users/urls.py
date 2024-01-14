
from django.urls import path, include
from .views import register_user, login_user, logout_user, token_check, get_user_data

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('user_data/', get_user_data, name='user_data'),
    path('token_check/', token_check, name='token_check')
]