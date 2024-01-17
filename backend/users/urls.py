
from django.urls import path, include
from .views import register_user, login_user, logout_user, token_check, get_user_data, get_user_by_id, edit_username

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('user_data/', get_user_data, name='user_data'),
    path('token_check/', token_check, name='token_check'),
    path('get_user_by_id/<int:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('edit_username/', edit_username, name='edit_usernames')
]