from flask import Flask
from flask_cors import CORS
from flask_restful import reqparse, Api, Resource
from utils.logger import logger
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS
from itsdangerous import BadSignature, BadData, BadHeader, BadPayload, BadTimeSignature

app = Flask(__name__)
CORS(app, supports_credentials=False)
app.config["JWT_SECRET_KEY"] = "my-super-secret"  # Change this!
app.config["JWT_HEADER_TYPE"] = ""
app.config["JWT_HEADER_NAME"] = "Authorization"
tjw_access_token = TJWSS(app.config["JWT_SECRET_KEY"], 60 * 5)
tjw_refresh_token = TJWSS(app.config["JWT_SECRET_KEY"], 60 * 60 * 24 * 30)


def create_access_token(identity: str = None) -> str:
    if identity is None:
        return ""
    return tjw_access_token.dumps(identity).decode()


def create_refresh_token(identity: str = None) -> str:
    if identity is None:
        return ""
    return tjw_refresh_token.dumps(identity).decode()


def args_required_method(parser):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            # logger.warning(f"warpper now: {fn}, {dir(fn)}")
            # if '__inner__' in dir(fn):
            #     logger.error(f"{fn.__inner__}")
            if 'Resource.dispatch_request' in str(fn) or \
                    ('__args_not_required__' in dir(fn) and fn.__args_not_required__ is True) or \
                    ('__inner__' in dir(fn) and (
                            "Resource.dispatch_request" in str(fn.__inner__) or "__args_not_required__" in str(
                        fn.__inner__))):
                return fn(*args, **kwargs)
            args_ = parser.parse_args()
            logger.info(f'args: {args_}')
            return fn(*args, **kwargs)

        wrapper.__inner__ = fn
        return wrapper

    return decorator


def args_required(parser):
    def class_builder(cls):
        class NewClass(cls):
            def __getattribute__(self, item):
                attr = super(NewClass, self).__getattribute__(item)
                if '__' not in item and callable(attr):
                    return args_required_method(parser)(attr)
                return attr

        return NewClass

    return class_builder


def args_not_required(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    wrapper.__args_not_required__ = True
    return wrapper


def auth_not_required(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    wrapper.__auth_not_required__ = True
    return wrapper


auth_reqparse = reqparse.RequestParser()
auth_reqparse.add_argument('Authorization', type=str, required=True, location="headers",
                           help="You must set Authorization in headers to visit here")


def auth_required(cls):
    class NewClass(cls):
        def __getattribute__(self, item):
            attr = super(NewClass, self).__getattribute__(item)
            if '__' not in item and callable(attr):
                return auth_required_method(attr)
            return attr

    return NewClass


def auth_required_method(fn):
    def wrapper(*args, **kwargs):
        # logger.warning(f"  auth now: {fn}, {dir(fn)}")
        if 'Resource.dispatch_request' in str(fn) or (
                '__auth_not_required__' in dir(fn) and fn.__auth_not_required__ is True) or \
                ('__inner__' in dir(fn) and (
                        "Resource.dispatch_request" in str(fn.__inner__) or "__auth_not_required__" in str(
                    fn.__inner__))):
            return fn(*args, **kwargs)
        args_ = auth_reqparse.parse_args()
        logger.info(f"  auth args: {args_}, {fn.__inner__}")
        auth = args_.get(app.config["JWT_HEADER_NAME"], None)
        if auth is None:
            return {"message": "Auth plz!"}, 401
        try:
            data = tjw_access_token.loads(auth)
        except (BadSignature, BadData, BadHeader, BadPayload, BadTimeSignature) as e:
            return {"message": str(e)}, 422
        return fn(*args, **kwargs)

    wrapper.__inner__ = fn
    return wrapper


g_reqparse = reqparse.RequestParser()
g_reqparse.add_argument('ok', type=str, required=True, location="args",
                        help="Test ok plz")


# @auth_required()
class Login(Resource):
    # @auth_required_method(g_reqparse)
    @auth_not_required
    def get(self):
        # result = {'message': "OK"}
        # logger.warning(f"{result}")
        # return result
        return {
            'access_token': create_access_token(identity="test_user"),
            'refresh_token': create_refresh_token(identity="test_user")
        }


@auth_required
@args_required(g_reqparse)
class TestVisit(Resource):
    def get(self):
        return {"message": 'Done'}


api = Api(app)
api.add_resource(Login, '/login')
api.add_resource(TestVisit, '/test')

if __name__ == '__main__':
    app.run('0.0.0.0', port=8192, debug=False)
