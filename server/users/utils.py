from .models import Users

def is_user_exists(username):
    return Users.objects.filter(nickname=username).exists()

def is_email_taken(email):
    return Users.objects.filter(email=email).exists()
