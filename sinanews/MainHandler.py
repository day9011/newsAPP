#!/usr/lib/python
#coding=utf-8
__author__ = 'dinghanyu'

from tornado.web import RequestHandler
import tornado
import json
import mydb

class MainHandler(RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        db = mydb.Mydb()
        news = db.query_news()
        jsonstr = '{'
        i = 1
        for item in news:
            print
            jsonstr += '"news' + '%d'%i + '":' + json.dumps(item) + ','
            i += 1
        jsonstr = jsonstr[:-1]
        jsonstr += '}'
        print jsonstr
        self.write(jsonstr)
        self.finish()

    def post(self):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_argument(key)
        print post_data
        self.write('test for post')
        self.finish()
