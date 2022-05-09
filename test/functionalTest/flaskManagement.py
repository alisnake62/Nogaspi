from werkzeug.datastructures import FileStorage
import io

class FakeRequest:

    remote_addr = "0.0.0.0"
    method = 'POST'
    json = {}
    files = {}

    def __init__(self, args, files = None):
        self.json = args
        if files is not None:
            for fileKey, fileName in files.items():
                if len(fileName.split('.')) == 1: fileName += ".file"
                if len(fileName.split('.')) > 2: fileName = "testFile.file"
                self.files[fileKey] = FileStorage(
                    stream=io.BytesIO(b"This is a better file ever"),
                    filename=fileName,
                    content_type="application/json"
                )
        self.form = []

def generateRealFile(path, fileName):
    if len(fileName.split('.')) == 1: fileName += ".file"
    if len(fileName.split('.')) > 2: fileName = "testFile.file"
    file = FileStorage(
        stream=io.BytesIO(b"This file is generete to pytest"),
        filename=fileName,
        content_type="application/json"
    )
    file.save(f"{path}{fileName}")
