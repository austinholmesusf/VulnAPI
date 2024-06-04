class EndpointException(Exception):
    def __init__(self, message, http_code=503):
        self.message = message
        self.http_code = http_code
        super().__init__(self.message)

