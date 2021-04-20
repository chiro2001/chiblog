import time
import pymongo
from config import Constants


class DataBase:
    def __init__(self):
        self.client = None
        self.db = None
        self.col = None
        self.connect_init()

    def connect_init(self):
        if len(Constants.DATABASE_URI) > 0:
            self.client = pymongo.MongoClient(Constants.DATABASE_URI)
        else:
            self.client = pymongo.MongoClient()
        self.db = self.client.chiro

    def error_report(self, error):
        self.db.chiblog_bug.insert_one({'time': time.asctime(), 'error': error})


db = DataBase()

if __name__ == '__main__':
    # _db = DataBase()
    pass
