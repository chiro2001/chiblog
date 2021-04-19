from flask import Flask, request
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource
from auth.tjw_auth import auth_required, auth_required_method, auth_not_required_method
from utils.args_decorators import args_required, args_required_method
from utils.make_result import make_result


class User:
    args_regist = reqparse.RequestParser() \
        .add_argument("username", type=str, required=True, location=["json", ]) \
        .add_argument("password", type=str, required=True, location=["json", ])

    def get(self, uid: int):
        """
        获取 uid 对应用户信息
        :param uid: uid
        :return:
        """
        pass

    @args_required_method(args_regist)
    def post(self):
        """
        注册
        :json username: 用户名
        :json password: 密码
        :return:
        """
        pass

    @auth_required_method
    def put(self, uid: int):
        """
        更新用户信息
        :param uid: uid
        :return:
        """

    @auth_required_method
    def delete(self, uid: int):
        """
        注销
        :param uid: uid
        :return:
        """


class Session(Resource):
    args_login = reqparse.RequestParser() \
        .add_argument("username", type=str, required=True, location=["json", ]) \
        .add_argument("password", type=str, required=True, location=["json", ])

    # Login
    @args_required_method(args_login)
    def post(self):
        return make_result()

    @auth_required_method
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
