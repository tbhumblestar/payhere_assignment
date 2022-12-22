from rest_framework.exceptions import APIException
from rest_framework import status

class ShortURLNotValidError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ('This shortURL valid date is over')
    default_code = 'url not valid'