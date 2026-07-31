from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .exceptions import InvalidCredentialsException
class AuthService:

    @staticmethod
    def register_user(validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

    @staticmethod
    def login_user(username , password):

        user = authenticate(
            username=username,
            password=password,
        )

        if user is None:
            raise InvalidCredentialsException()

        refresh=RefreshToken.for_user(user)

        return{
            "user":user,
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }

