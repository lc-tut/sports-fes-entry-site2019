from rest_framework.exceptions import APIException as OriginalAPIException
from rest_framework import status


class APIException(OriginalAPIException):
    status_code = status.HTTP_400_BAD_REQUEST