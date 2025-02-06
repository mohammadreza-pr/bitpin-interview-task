from typing import Optional

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


class CustomException(APIException):

    status_code: int = status.HTTP_400_BAD_REQUEST
    default_detail: str = "Invalid input"
    default_code: str = "invalid"



def custom_exception_handler(
    exc: Exception, context: dict
) -> Optional[Response]:
    
    response = exception_handler(exc, context)

    if response is not None:
        error_code: str = getattr(exc, "default_code", "unknown")
        message: str = getattr(exc, "default_detail", "")

        error_response = {
            "error": response.data,  
            "code": error_code,  
            "message": message,  
        }
        response.data = error_response

    return response