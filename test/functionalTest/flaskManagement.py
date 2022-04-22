from werkzeug.datastructures import FileStorage

class FakeRequest:

    remote_addr = "0.0.0.0"
    method = 'POST'
    json = {}
    files = {}

    def __init__(self, args, file = None, keyFile = None):
        self.json = args
        if file is not None:
            fp = open(f"test/{file}", 'rb')
            file = FileStorage(fp, file, name=file.split('.')[0], content_type='image/jpg')
            self.files[keyFile] = file
