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
        status = ""
        try:
            status = self.response.status
        except AttributeError:
            status = self.response.status_code
        return f"Status {status}{message}"
