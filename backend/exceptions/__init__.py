from utils.logger import logger


class BlogBaseError(Exception):
    def __init__(self, data: str = None):
        self.data = data
        logger.error(self.__str__())

    def __str__(self):
        return f"Error: {self.__class__.__name__}{(' : %s' % self.data) if self.data is not None else ''}"


class BlogError(BlogBaseError):
    pass


class BlogPermissionError(BlogBaseError):
    pass


class BlogLoginError(BlogBaseError):
    pass


class BlogUserExist(BlogBaseError):
    pass


class BlogContentExist(BlogBaseError):
    pass
