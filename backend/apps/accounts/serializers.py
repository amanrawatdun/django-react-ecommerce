from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User
from .services import AuthService

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True , validators=[validate_password])

    class Meta:
        model=User
        fields=['username','email','password']

    def validate_email(self , value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email is already registered. "
            )
        return value

    def validate_password_field(self , value):
        validate_password(value)
        return value
    
    def create(self , validated_data):
        return AuthService.register_user(validated_data)

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField( write_only=True)
