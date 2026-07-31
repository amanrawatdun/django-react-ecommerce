from rest_framework.exceptions import APIException
from rest_framework import status

class InvalidCredentialsException(APIException):
    
    status_code = status.HTTP_401_UNAUTHORIZED

    default_detail = "Invalid username or password."

    default_code = "invalid_credentials"