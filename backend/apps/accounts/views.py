from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView , GenericAPIView
from rest_framework.response import Response


from .serializers import RegisterSerializer , LoginSerializer
from .services import AuthService



class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self , request , *args , **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user=serializer.save()

        return Response(
            {
                "success":True,
                "message":"User registered successfully",
                "data":{
                    "id":user.id,
                    "username":user.username,
                    "email":user.email,
                },
            },
            status=status.HTTP_201_CREATED,
        )

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self , request , *args , **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result=AuthService.login_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        
        return Response(
            {
                "success": True,
                "message": "Login successful.",
                "data": {
                    "user": {
                        "id": result["user"].id,
                        "username": result["user"].username,
                        "email": result["user"].email,
                    },
                    "tokens": {
                        "access": result["access"],
                        "refresh": result["refresh"],
                    },
                },
            },
            status=status.HTTP_200_OK,
        )

def profile(request):
    return Response({
        "message":f"this is profile of {request.user.username}"
    })
