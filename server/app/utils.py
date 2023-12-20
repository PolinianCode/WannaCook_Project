from .models import Users, Favorites

def is_user_exists(username):
    return Users.objects.filter(nickname=username).exists()

def is_email_taken(email):
    return Users.objects.filter(email=email).exists()

def is_favorite_exists(recipe_id, user_id):
    return Favorites.objects.filter(recipe_id=recipe_id, user_id=user_id).exists()
