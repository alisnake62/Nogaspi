from .apiResponse import APIException

class RegisterException(APIException):
    pass

class DBException(APIException):
    pass

class TokenException(APIException):
    pass

class EmptyException(APIException):
    pass

class InputAPIException(APIException):
    pass