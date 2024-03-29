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

class OpenFoodException(APIException):
    pass

class OpenRouteServiceException(APIException):
    pass

class DonationException(APIException):
    pass

class CoordException(APIException):
    pass

class UserException(APIException):
    pass

class FridgeException(APIException):
    pass

class ConversationException(APIException):
    pass

class FileException(APIException):
    pass