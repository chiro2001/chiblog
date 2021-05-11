from flask import Flask, request
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource

from config import Constants
from apis.users import UserUid, User, Session
from apis.content import Content, ContentCid, ContentTree
from flask_pymongo import PyMongo
from database.database import set_mongo

app_name = 'apis'
app = Flask(app_name)
app.config.update(
    MONGO_URI=Constants.DATABASE_URI
)
# 设置可跨域访问；因为要用JWT，就不需要supports_credentials来支持Cookies了
CORS(app, supports_credentials=False)
# 设置MongoDB扩展
set_mongo(PyMongo(app))

api = Api(app)
api.add_resource(User, "/user")
api.add_resource(UserUid, "/user/<int:uid>")
api.add_resource(Session, "/session")
api.add_resource(ContentCid, "/content/<int:cid>")
api.add_resource(ContentTree, "/content/tree")
api.add_resource(Content, "/content")

if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=False)
