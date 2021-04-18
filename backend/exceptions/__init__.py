from utils.logger import logger


class BlogBaseError(Exception):
    def __init__(self, data):
        self.data = data
        logger.error(self.__str__())

    def __str__(self):
        return f"Error: {self.__class__.__name__} : {self.data}"


class BlogError(BlogBaseError):
    pass


class BlogPermissionError(BlogBaseError):
    pass


class BlogLoginError(BlogBaseError):
    pass
