from database.tools import *


class Session:
    def __init__(self, d):
        self.d = d
        self.col: pymongo.collection.Collection = d.session

    def get_by_uid(self, uid: int) -> dict or None:
        return find_one(self.col, {'uid': uid})

    def check_password(self, uid: int, password: str) -> bool:
        user_data = find_one(self.col, {'uid': uid, 'password': password})
        if user_data is None:
            return False
        if user_data.get('password') != password:
            return False
        return True

    def update_one(self, session: dict) -> bool:
        uid = session.get('uid')
        session_data = self.get_by_uid(uid)
        if session_data is None:
            return False
        print('session_data', json_dumps_format(session_data))
        print('session', json_dumps_format(session))
        if 'created_at' in session_data:
            del session_data['created_at']
        dict_update(session_data, session)
        return auto_time_update(self.col, {'uid': uid}, session_data)

    def update_login(self, uid: int) -> bool:
        session = self.get_by_uid(uid)
        if session is None:
            return False
        if 'created_at' in session:
            del session['created_at']
        session['last_login'] = datetime.datetime.utcnow()
        return self.update_one(session)

    def insert(self, uid: int, password: str):
        auto_time_update(self.col, {'uid': uid}, {'uid': uid, 'password': password})

    def remove(self, uid: int):
        self.col.delete_one({'uid': uid})
