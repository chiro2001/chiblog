from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
# 设置可跨域访问
# 因为要用JWT，就不需要supports_credentials来支持Cookies了
CORS(app, supports_credentials=False)


def test():
    """
    :param:
    :return:
    """
    pass


if __name__ == '__main__':
    print(dir(test))
    print(test.__doc__)
