def apiResponse(request, data = None, exception : bool = False, status_code = 200):
    
    if exception: summary = "Exception"
    else : summary = "Ok"
    
    metadata = {
        'url': request.url,
        'method' : request.method,
        'inputJson': request.json,
        'summary': summary,
        'status_code': status_code
    }
    json = {
        'metadata': metadata,
        'data': data
    }

    return json
    

class APIException(Exception):
    status_code = 400

    def __init__(self, message, request, status_code=None):
        Exception.__init__(self)
        self.message = message
        self.request = request
        if status_code is not None:
            self.status_code = status_code

    def response(self):
        data = {
            'exception' : self.__class__.__name__,
            'message' : self.message
        }
        return apiResponse(request = self.request, data=data, exception=True, status_code=self.status_code)