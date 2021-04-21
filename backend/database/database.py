import time
from utils.logger import logger
from database.tools import *
from database.user import User
from database.session import Session
from database.content import Content


class DataBase:
    COLLECTIONS = [
        'user', 'user_uid', 'chiblog_bug', 'session', 'content', 'content_cid'
    ]

    def __init__(self):
        self.client = None
        self.db = None
        self.connect_init()
        self.user: User = None
        self.session: Session = None
        self.content: Content = None
        self.init_parts()
        if Constants.RUN_REBASE:
            self.rebase()

    def init_parts(self):
        self.user = User(self.db)
        self.session = Session(self.db)
        self.content = Content(self.db)

    def rebase(self):
        for col in DataBase.COLLECTIONS:
            logger.info(f'Dropping {col}')
            self.db[col].drop()
        self.init_parts()
        self.user.insert(Constants.USERS_OWNER)

    def connect_init(self):
        if len(Constants.DATABASE_URI) > 0:
            self.client = pymongo.MongoClient(Constants.DATABASE_URI)
        else:
            self.client = pymongo.MongoClient()
        self.db = self.client.chiro

    def error_report(self, error):
        self.db.chiblog_bug.insert_one({'time': time.asctime(), 'error': error})


mongo = None


def set_mongo(mongo_):
    global mongo
    mongo = mongo_


db = DataBase()

if __name__ == '__main__':
    pass
    db.rebase()
    db.session.insert('chiro', '3521')
    logger.info(db.session.find_by_username('chiro'))
    logger.info(db.session.check_password('chiro', '3521'))
