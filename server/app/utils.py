from .models import Users

def check_user_exist(username):
    return Users.objects.filter(nickname=username).exists()


def check_user_email_exist(email):
    return Users.objects.filter(email=email).exists()