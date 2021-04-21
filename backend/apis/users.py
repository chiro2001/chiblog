from flask_restful import reqparse, abort, Api, Resource
from auth.tjw_auth import *
from utils.args_decorators import args_required, args_required_method
from utils.make_result import make_result
from utils.logger import logger
from utils.password_check import password_check
from database.database import mongo, db
from config import Statics
import exceptions
import json


class User(Resource):
    args_signin = reqparse.RequestParser() \
        .add_argument("username", type=str, required=True, location=["json", ]) \
        .add_argument("password", type=str, required=True, location=["json", ])

    # TODO: 此处可能并非线程安全！使用的 args_signin 是静态变量
    @args_required_method(args_signin)
    def post(self):
        """
        注册
        :json username: 用户名
        :json password: 密码
        :return:
        """
        args = self.args_signin.parse_args()
        username, password = args.get('username'), args.get('password')
        result, text = password_check(password)
        if not result:
            return make_result(400, message=text)
        # check_result = db.session.check_password(username=username, password=password)
        # if not check_result:
        #     return make_result(403)
        try:
            uid = db.user.insert({
                'username': username,
                'nick': username,
                'level': 1,
                'state': 'normal',
                'profile': {}
            })
        except exceptions.BlogUserExist:
            return make_result(400, message='用户已存在')
        db.session.insert(uid, password)
        return make_result(data={'uid': uid})


class UserUid(Resource):
    def get(self, uid: int):
        """
        获取 uid 对应用户信息
        :param uid: uid
        :return:
        """
        user = db.user.get_by_uid(uid)
        return make_result(data={'user': user})

    @auth_required_method
    def put(self, uid: int):
        """
        更新用户信息
        :param uid: uid
        :return:
        """
        user = reqparse.RequestParser().parse_args()
        user['uid'] = uid
        result = db.user.update_one(user)
        if not result:
            return make_result(400)
        return make_result()

    @auth_required_method
    def delete(self, uid: int):
        """
        删除自己用户
        :param uid: uid
        :return:
        """
        db.user.delete_user(uid)
        return make_result()


class Session(Resource):
    args_login = reqparse.RequestParser() \
        .add_argument("username", type=str, required=True, location=["json", ]) \
        .add_argument("password", type=str, required=True, location=["json", ])
    args_update = reqparse.RequestParser() \
        .add_argument("refresh_token", type=str, required=True, location=["json", ])
    args_update_password = reqparse.RequestParser() \
        .add_argument("password")

    # Login
    @args_required_method(args_login)
    def post(self):
        args = self.args_login.parse_args()
        username, password = args.get('username'), args.get('password')
        user = db.user.find_by_username(username=username)
        if user is None:
            return make_result(403)
        uid = user.get('uid')
        result = db.session.check_password(uid=uid, password=password)
        if not result:
            return make_result(403)
        db.session.update_login(uid)
        token_payload = {'uid': uid}
        access_token = create_access_token(token_payload)
        refresh_token = create_refresh_token(token_payload)
        return make_result(data={'access_token': access_token, 'refresh_token': refresh_token})

    # 更新密码
    @args_required_method(args_update_password)
    def put(self, uid: int):
        password = self.args_update_password.parse_args().get('password')
        if not db.session.update_one(uid, password):
            return make_result(400)
        return make_result()

    @args_required_method(args_update)
    def get(self):
        """
        更新 access_token
        :return:
        """
        refresh_token = self.args_update.parse_args().get('refresh_token')
        try:
            data = Statics.tjw_refresh_token.loads(refresh_token)
        except (BadSignature, BadData, BadHeader, BadPayload) as e:
            return make_result(422, message=f"Bad token: {e}")
        except BadTimeSignature:
            return make_result(424)
        uid = data.get('uid')
        payload = {
            'uid': uid
        }
        access_token = create_access_token(payload)
        refresh_token_new = create_refresh_token(payload)
        return make_result(data={
            'access_token': access_token,
            'refresh_token': refresh_token_new
        })

    @auth_required_method
    def delete(self, uid: int):
        """
        注销
        :return:
        """
        return make_result()
