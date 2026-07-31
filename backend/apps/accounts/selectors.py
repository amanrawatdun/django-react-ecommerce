from .models import User

def get_user_by_username(username):

    return User.objects.filter(
        username=username
    ).first()


def get_user_by_email(email):

    return User.objects.filter(
        email=email
    ).first()
