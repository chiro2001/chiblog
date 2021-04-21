import pymongo
import datetime
from config import Constants
from utils.formats import json_dumps_format


def dict_update(dist: dict, src: dict) -> dict:
    result = dist
    for k in src:
        v = src[k]
        if k in dist:
            if type(dist[k]) is type(dict):
                result[k] = dict_update(dist[k], v)
            else:
                result[k] = v
        else:
            dist[k] = v
    return result


def insert_id_if_not_exist(col: pymongo.collection.Collection, key_name: str, value):
    result = col.find_one({"_id": key_name})
    if result is None:
        col.insert_one({"_id": key_name, "sequence_value": value})


def auto_time_insert(col: pymongo.collection.Collection,
                     insert_dict: dict):
    dt0 = datetime.datetime.utcnow()
    insert_dict['created_at'] = dt0
    return col.insert_one(insert_dict)


def auto_time_update(col: pymongo.collection.Collection,
                     filter_dict: dict, update_dict: dict):
    dt0 = datetime.datetime.utcnow()
    update_dict['updated_at'] = dt0
    update_dict = {'$set': update_dict, '$setOnInsert': {'created_at': dt0}}
    return col.update_one(filter_dict, update_dict, upsert=True)


def find_one(col: pymongo.collection.Collection,
             filter_dict: dict, include_id: bool = False) -> dict or None:
    result = col.find_one(filter_dict, {"_id": 1 if include_id else 0})
    if result is None:
        return None
    return dict(result)


def find_many(col: pymongo.collection.Collection,
              filter_dict: dict,
              sort_by: str = None,
              reverse: bool = False,
              limit: int = Constants.FIND_LIMIT,
              offset: int = 0,
              include_id: bool = False) -> list:
    result = col.find(filter_dict, {"_id": 1 if include_id else 0})
    if sort_by is not None:
        result = result.sort(sort_by, pymongo.DESCENDING if reverse else pymongo.ASCENDING)
    result = result.skip(offset).limit(limit)
    return list(result)
