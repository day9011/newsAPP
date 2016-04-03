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

def data_to_json(pre, cursor, news):
    jsonstr = '{'
    jsonstr += '"pre": %s,' % (str(pre).lower())
    jsonstr += '"current_cursor": %d,' % (cursor)
    if news == []:
        jsonstr += '"news": []'
    else:
        jsonstr += '"news":['
    for item in news:
        jsonstr += json.dumps(item) + ','
    jsonstr = jsonstr[:-1]
    jsonstr += ']}'
    return jsonstr

def handle_query_result(news):
    newsresults = []
    for item in news:
        newsitem = newsData().data
        newsitem['cursor'] = item[0]
        newsitem['id'] = item[1]
        newsitem['url'] = item[2]
        newsitem['date'] = item[3]
        newsitem['source'] = item[4]
        newsitem['title'] = item[5]
#       newsitem['content'] = item[6]
        newsitem['content'] = ""
        newsitem['abstract'] = item[7]
        newsitem['keywords'] = item[8]
        newsitem['image'] = item[9]
        newsresults.append(newsitem)
    return newsresults
