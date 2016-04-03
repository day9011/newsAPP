#!/usr/lib/python
#coding=utf-8
__author__ = 'dinghanyu'

from tornado.web import RequestHandler
from news_model import data_to_json
import tornado
import mydb

class news_abstract(RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        db = mydb.Mydb()
 #       news = db.query_news('SELECT news_attribute.*, news_contents.news_abstract FROM news_attribute, news_contents WHERE news_attribute.news_id = news_contents.news_id')
        news = db.query_news()
        cursor = news[0]['cursor']
        returndata = data_to_json(True, cursor, news)
        self.write(returndata)
        self.finish()

