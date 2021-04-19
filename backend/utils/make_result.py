from flask import jsonify
from config import Constants


class ResultRules:
    code_message = {
        200: "OK",
        400: "Bad Request",
        401: Constants.JWT_MESSAGE_401,
        404: "The Requested URL Was Not Found",
        403: "Forbidden",
        500: "Internal Server Error",
    }


def make_result(code=200, message=None, data=None):
    result = {
        'code': code,
        'data': {},
        'message': message
    }
    if result['message'] is None:
        del result['message']
    if code != 200:
        result['error'] = ResultRules.code_message.get(code, "Unknown Error")
    if data is not None:
        result['data'] = data
    return result, code
