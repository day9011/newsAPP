__author__ = 'dinghanyu'
#!/usr/lib/python
#coding=utf-8
import json
import operator

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
    news = sorted(news, key=operator.itemgetter('cursor'), reverse = True)
    c_cursor = news[0]["cursor"]
    jsonstr = '{'
    jsonstr += '"pre": %s,' % (str(pre))
    jsonstr += '"current_cursor": %d,' % (c_cursor)
    jsonstr += '"news":['
    for item in news:
        jsonstr += json.dumps(item) + ','
    jsonstr = jsonstr[:-1]
    jsonstr += ']}'
    return jsonstr
