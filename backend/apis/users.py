from flask import Flask, request
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource
from auth.tjw_auth import auth_required, auth_required_method, auth_not_required_method
from utils.args_decorators import args_required, args_required_method
from utils.make_result import make_result
from utils.logger import logger
from utils.password_check import password_check
from database.database import db


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



class UserUid(Resource):
    args_signin = reqparse.RequestParser() \
        .add_argument("username", type=str, required=True, location=["json", "args"]) \
        .add_argument("password", type=str, required=True, location=["json", "args"])

    @args_required_method(args_signin)
    def get(self, uid: int):
        """
        获取 uid 对应用户信息
        :param uid: uid
        :return:
        """
        logger.info(f"get uid:{uid}, args: {UserUid.args_signin.parse_args()}")
        return make_result(data=UserUid.args_signin.parse_args())

    @auth_required_method
    def put(self, uid: int):
        """
        更新用户信息
        :param uid: uid
        :return:
        """
        pass

    @auth_required_method
    def delete(self, uid: int):
        """
        注销
        :param uid: uid
        :return:
        """
        pass


class Session(Resource):
    args_login = reqparse.RequestParser() \
        .add_argument("username", type=str, required=True, location=["json", ]) \
        .add_argument("password", type=str, required=True, location=["json", ])
    args_update = reqparse.RequestParser() \
        .add_argument("refresh_token", type=str, required=True, location=["json", ])

    # Login
    @args_required_method(args_login)
    def post(self):
        return make_result()

    @args_required_method(args_update)
    def get(self):
        """
        获取会话信息(?)
        :return:
        """

    @auth_required_method
    def delete(self):
        """
        注销
        :return:
        """
