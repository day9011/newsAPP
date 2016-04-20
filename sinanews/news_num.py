#!/usr/lib/python
#coding=utf-8
__author__ = 'dinghanyu'

from tornado.web import RequestHandler
from news_model import *
import tornado
import mydb
from writeToLog import *

class news_num(RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET,POST")
        self.set_header("Access-Control-Allow-Headers", "day9011")
        self.set_header("Access-Control-Max-Age", "172800")
        self.set_header("Access-Control-Allow-Credentials", "true")
        returndata = ""
        c_cursor = ""
        pre = False
        db = mydb.Mydb()
        news = []
 #       news = db.query_news('SELECT news_attribute.*, news_contents.news_abstract FROM news_attribute, news_contents WHERE news_attribute.news_id = news_contents.news_id')
        min_cursor = db.query_news('SELECT min(news_cursor) FROM news_detail')[0][0]
        try:
            c_cursor = int(self.get_argument('cursor'))
            num_news = int(self.get_argument('num'))
        except Exception, e:
            error_log('get cursor or num error')
            return
        if int(min_cursor) >= int(c_cursor):
            returndata = data_to_json(True, min_cursor, [])
        else:
            D_value = int(c_cursor) - int(min_cursor)
            sql_str = 'select * from news_detail where news_cursor < %d order by news_cursor desc' % (c_cursor)
            if D_value < num_news:
                news = db.query_news(sql_str, D_value)
                news = handle_query_result(news)
                cursor = news[D_value - 1]['cursor']
                pre = True
                returndata = data_to_json(pre, cursor, news)
            else:
                news = db.query_news(sql_str, num_news)
                news = handle_query_result(news)
                cursor = news[num_news - 1]['cursor']
                if int(cursor) == int(min_cursor):
                    pre = True
                returndata = data_to_json(pre, cursor, news)
#        news = db.query_news()
#        news = sorted(news, key=lambda obj:obj.get('cursor'), reverse=True)
#        cursor = news[0]['cursor']
#        returndata = data_to_json(True, cursor, news)
        self.write(returndata)
        self.finish()

