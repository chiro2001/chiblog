import json
import datetime


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            # return obj.strftime('%Y-%m-%d %H:%M:%S')
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            # return obj.strftime('%Y-%m-%d')
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def json_dumps_format(data: dict):
    return json.dumps(data, cls=DateTimeEncoder, ensure_ascii=False, indent=2)
