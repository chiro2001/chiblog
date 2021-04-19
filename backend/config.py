import os
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS


class Constants:
    # Version info
    VERSION = "0.0.1"
    AUTHOR = "Chiro"
    EMAIL = "Chiro2001@163.com"
    # JWT config
    JWT_SECRET_KEY = "HeyThisIsAStrangeStringChiro3521#*&"
    JWT_HEADER_TYPE = ""
    JWT_HEADER_NAME = "Authorization"
    JWT_LOCATIONS = ['headers', ]
    JWT_MESSAGE_401 = "Authorization required in head"
    JWT_ACCESS_TIME = 60 * 5
    JWT_REFRESH_TIME = 60 * 60 * 24 * 30
    # API config
    API_PATH = '/api/v1'
    # Running config
    RUN_LISTENING = "0.0.0.0"
    RUN_PORT = int(os.environ.get("PORT", 8192))
    RUN_USE_RELOAD = False



class Statics:
    tjw_access_token = TJWSS(Constants.JWT_SECRET_KEY, Constants.JWT_ACCESS_TIME)
    tjw_refresh_token = TJWSS(Constants.JWT_SECRET_KEY, Constants.JWT_REFRESH_TIME)
