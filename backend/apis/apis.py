from flask import Flask, request
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource

from apis.users import UserUid, User, Session

app_name = 'apis'
app = Flask(app_name)
# 设置可跨域访问；因为要用JWT，就不需要supports_credentials来支持Cookies了
CORS(app, supports_credentials=False)

api = Api(app)
api.add_resource(User, "/user")
api.add_resource(UserUid, "/user/<int:uid>")
api.add_resource(Session, "/session")


if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=False)
