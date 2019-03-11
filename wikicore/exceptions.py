class WikiException(Exception):
    """Base class for exceptions in this module"""
    def __init__(self, message):
        self.message = message

class WikiPageNotFound(WikiException):
    """The wiki page was not found"""
