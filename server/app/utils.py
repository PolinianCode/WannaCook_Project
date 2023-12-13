from .models import Users, Favorites

def check_user_exist(username):
    return Users.objects.filter(nickname=username).exists()


def check_user_email_exist(email):
    return Users.objects.filter(email=email).exists()


def check_user_favorites_exists(recipe_id, user_id):
    return Favorites.objects.filter(recipe_id=recipe_id, user_id=user_id).exists()