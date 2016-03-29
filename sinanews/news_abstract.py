#!/usr/lib/python
#coding=utf-8
__author__ = 'dinghanyu'

from tornado.web import RequestHandler
import tornado
import json
import mydb

class news_abstract(RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        db = mydb.Mydb()
 #       news = db.query_news('SELECT news_attribute.*, news_contents.news_abstract FROM news_attribute, news_contents WHERE news_attribute.news_id = news_contents.news_id')
        news = db.query_news()
        jsonstr = '{'
        jsonstr += '"pre": true,'
        jsonstr += '"current_cursor": 2,'
        jsonstr += '"news":['
        for item in news:
            jsonstr += json.dumps(item) + ','
        jsonstr = jsonstr[:-1]
        jsonstr += ']}'
        self.write(jsonstr)
        self.finish()

    def post(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_argument(key)
        print post_data
        self.write('test for post')
        self.finish()
