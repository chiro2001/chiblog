from flask_restful import reqparse
from itsdangerous import BadSignature, BadData, BadHeader, BadPayload, BadTimeSignature
from utils.logger import logger
from utils.make_result import make_result
from config import Statics, Constants


def create_access_token(identity: str = None) -> str:
    if identity is None:
        return ""
    return Statics.tjw_access_token.dumps(identity).decode()


def create_refresh_token(identity: str = None) -> str:
    if identity is None:
        return ""
    return Statics.tjw_refresh_token.dumps(identity).decode()


auth_reqparse = reqparse.RequestParser()
auth_reqparse.add_argument(Constants.JWT_HEADER_NAME, type=str, required=True, location=Constants.JWT_LOCATIONS,
                           help=Constants.JWT_MESSAGE_401)


def auth_required(cls):
    class NewClass(cls):
        def __getattribute__(self, item):
            attr = super(NewClass, self).__getattribute__(item)
            if '__' not in item and callable(attr):
                return auth_required_method(attr)
            return attr

    return NewClass


def auth_not_required_method(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    wrapper.__auth_not_required__ = True
    return wrapper


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
        auth = args_.get(Constants.JWT_HEADER_NAME, None)
        if auth is None:
            return make_result(401)
        try:
            data = Statics.tjw_access_token.loads(auth)
        except (BadSignature, BadData, BadHeader, BadPayload, BadTimeSignature) as e:
            return make_result(422, message=f"Bad token: {e}")
        logger.info(f"data: {data}")
        return fn(*args, **kwargs)

    wrapper.__inner__ = fn
    return wrapper
