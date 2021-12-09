from .logging import logging
from datetime import datetime

def apiResponse(request, data = None, exception : bool = False, status_code = 200):
    if data is None: data = {}
    if exception: summary = "Exception"
    else : summary = "Ok"
    
    metadata = {
        'url': request.url,
        'method' : request.method,
        'inputJson': request.json,
        'summary': summary,
        'status_code': status_code
    }
    data['metadata'] = metadata

    return data
    

class APIException(Exception):
    status_code = 400

    def __init__(self, messageAPI, messageLog, request, status_code=None):
        Exception.__init__(self)
        self.messageAPI = messageAPI
        self.messageLog = messageLog
        self.request = request
        if status_code is not None:
            self.status_code = status_code
        errorLine = request.remote_addr + " - - " + self.__class__.__name__ + " - " + messageLog
        logging.error(errorLine)
        print(str(datetime.now()) + " - ERROR - " + errorLine)

    def response(self):
        data = {
            'exception' : self.__class__.__name__,
            'message' : self.messageAPI
        }
        return apiResponse(request = self.request, data=data, exception=True, status_code=self.status_code)