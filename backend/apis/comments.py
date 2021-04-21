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


class Comments(Resource):
    pass

