class FakeRequest:

    remote_addr = "0.0.0.0"
    method = 'POST'
    json = {}

    def __init__(self, args):
        self.json = args