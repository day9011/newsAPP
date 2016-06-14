#!/usr/lib/python
#coding=utf-8
__author__ = 'dinghanyu'

from tornado.web import RequestHandler
from utils.news_model import *
import tornado
from lib.db import Mydb
from utils.news_log import getlogger
import json

__all__ = ['news_num']
logger = getlogger()

class news_num(RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        try:
            info = self.request.protocol + "://" + self.request.host + ", method=" + self.request.method + ", access url=" + self.request.uri
            logger.info(info)
            returndata = ""
            c_cursor = ""
            pre = False
            db = Mydb()
            news = []
            s, max_cursor = db.get('SELECT max(news_cursor) as max_cursor FROM news_detail')
            if s:
                raise Exception("cant get max cursor")
            else:
                max_cursor = max_cursor[0]['max_cursor']
            try:
                c_cursor = int(self.get_argument('cursor'))
                num_news = int(self.get_argument('num'))
            except:
                logger.error('get cursor or num error')
                raise Exception('get cursor or num error')
            if int(max_cursor) <= int(c_cursor):
                returndata = news_to_json(True, max_cursor, [])
            else:
                D_value = int(max_cursor) - int(c_cursor)
                sql_str = 'SELECT news_cursor as n_cursor, news_source as source, news_url as url, news_keywords as keywords, ' \
                          'news_title as title, news_date as date, news_abstract as abstract, news_image as image, news_id as' \
                          ' id FROM news_detail WHERE news_cursor > %d ORDER BY news_cursor LIMIT ' % (c_cursor)
                if D_value < num_news:
                    sql_str += str(D_value)
                    s, news = db.get(sql_str)
                    if s:
                        raise Exception("cant get news data")
                    cursor = news[len(news) - 1]['n_cursor']
                    returndata = news_to_json(True, cursor, news)
                else:
                    sql_str += str(num_news)
                    s, news = db.get(sql_str)
                    if s:
                        raise Exception("cant get max news data")
                    cursor = news[len(news) - 1]['n_cursor']
                    if int(cursor) == int(max_cursor):
                        pre = True
                    returndata = news_to_json(pre, cursor, news)
    #        news = db.query_news()
    #        news = sorted(news, key=lambda obj:obj.get('cursor'), reverse=True)
    #        cursor = news[0]['cursor']
    #        returndata = news_to_json(True, cursor, news)
        except Exception, e:
            logger.error(str(e))
            returndata = json.dumps({'status' : '-100', 'content' : str(e)})
        finally:
            self.write(returndata)
            self.finish()

