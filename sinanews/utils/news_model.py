__author__ = 'dinghanyu'
#!/usr/lib/python
#coding=utf-8
import json

__all__ = ['newsData', 'news_to_json']

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

def news_to_json(pre, cursor, news):
    jsonstr = '{'
    jsonstr += '"pre": %s,' % (str(pre).lower())
    jsonstr += '"current_cursor": %d,' % (cursor)
    if news == []:
        jsonstr += '"news": []'
    else:
        jsonstr += '"news":['
    for item in news:
        item['cursor'] = item['n_cursor']
        item.pop('n_cursor')
        jsonstr += json.dumps(item) + ','
    jsonstr = jsonstr[:-1]
    jsonstr += ']}'
    return jsonstr



