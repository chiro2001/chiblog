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


class ContentTree(Resource):
    def get(self):
        """
        获取内容的树状path
        :return:
        """
        root = db.content.get_tree_root()
        return make_result(data={'tree': root})


class Content(Resource):
    args_list_content = reqparse.RequestParser() \
        .add_argument("filters", type=list, required=False, location=['json', 'args']) \
        .add_argument("sort_by", type=dict, required=False, location=['json', 'args']) \
        .add_argument("reverse", type=bool, required=False, location=['json', 'args']) \
        .add_argument("limit", type=int, required=False, location=['json', 'args']) \
        .add_argument("offset", type=int, required=False, location=['json', 'args'])
    args_post_content = reqparse.RequestParser() \
        .add_argument("title", type=str, required=True, location=['json', ]) \
        .add_argument("content", type=str, required=True, location=['json', ]) \
        .add_argument("password", type=str, required=False, location=['json', ]) \
        .add_argument("level", type=int, required=False, location=['json', ])

    @args_required_method(args_list_content)
    def get(self):
        """
        获取发布的内容列表
        :return:
        """
        args = self.args_list_content.parse_args()
        filters = args.get('filters')
        filters = {} if filters is None else filters
        args = {k: args[k] for k in args if args[k] is not None}
        kwargs = {}
        kws = ['sort_by', 'limit', 'offset', 'reverse']
        for k in kws:
            if k in args:
                kwargs[k] = args[k]
        # TODO: 检查 filter 是否合法
        result = db.content.find(filters, **kwargs)
        return make_result(data={'content_list': result})

    @auth_required_method
    @args_required_method(args_post_content)
    def post(self, uid: int):
        """
        发布新内容
        :return:
        """
        content = self.args_post_content.parse_args()
        content = {k: content[k] for k in content if content[k] is not None}
        content['author'] = uid
        cid = db.content.insert(content)
        return make_result(data={'cid': cid})


class ContentCid(Resource):
    args_visit_content = reqparse.RequestParser() \
        .add_argument("password", type=str, required=False, location=['json', ])

    @args_required_method(args_visit_content)
    def get(self, cid: int):
        """
        获取发布的内容
        :param cid:
        :return:
        """
        content = db.content.get_by_cid(cid)
        if content is None:
            return make_result(404)
        if 'password' not in content:
            return make_result(data={'content': content})
        password = self.args_visit_content.parse_args().get("password")
        if password != content['password']:
            return make_result(403)
        return make_result(data={'content': content})
