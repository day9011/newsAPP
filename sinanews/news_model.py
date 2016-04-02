__author__ = 'dinghanyu'
#!/usr/lib/python
#coding=utf-8
import json

class newsData:
    def __init__(self):
        self.data = {
            "cursor": int,
            "id" : "",
            "source" : "",
            "date" : "",
            "url" : "",
            "title" : "",
            "content" : "",
            "keywords" : "",
            "abstract" : "",
            "image" : "",
        }

def data_to_json(pre, news):
    jsonstr = '{'
    jsonstr += '"pre": true,'
    jsonstr += '"current_cursor": 2,'
    jsonstr += '"news":['
    for item in news:
        jsonstr += json.dumps(item) + ','
    jsonstr = jsonstr[:-1]
    jsonstr += ']}'
    return jsonstr
