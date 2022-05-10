from werkzeug.datastructures import FileStorage
import io

def generateFile(fileName):
    return FileStorage(
        stream=io.BytesIO(b"This file is generete to pytest"),
        filename=fileName,
        content_type="application/json"
    )

def generateAndSaveFile(path, fileName):
    file = generateFile(fileName)
    file.save(f"{path}{fileName}")

class FakeRequest:

    remote_addr = "0.0.0.0"
    method = 'POST'
    json = {}
    files = {}
    form = []

    def __init__(self, args, files = None):
        self.json = args
        if files is not None:
            self.files = {key: generateFile(fileName) for key, fileName in files.items()}