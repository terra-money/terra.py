"""Terra SDK-specific errors and exceptions."""


class LCDResponseError(IOError):
    """Triggered when response from LCD is not 2xx status code"""

    def __init__(self, message, response):
        self.message = message
        self.response = response

    def __str__(self):
        message = ""
        if self.message:
            message = " - " + self.message
        return f"Status {self.response.status}{message}"
