#coding:utf-8
import json
from datetime import datetime

class JsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, o)
