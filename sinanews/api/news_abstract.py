#!/usr/lib/python
#coding=utf-8
__author__ = 'dinghanyu'

from tornado.web import RequestHandler
from utils.news_model import news_to_json
import tornado
from utils.db_func import query_news
from utils.news_log import getlogger
import json

__all__ = ['news_abstract']
logger = getlogger()

class news_abstract(RequestHandler):
    @tornado.web.asynchronous
    def get(self):
 #       news = db.query_news('SELECT news_attribute.*, news_contents.news_abstract FROM news_attribute, news_contents WHERE news_attribute.news_id = news_contents.news_id')
        returndata = ''
        try:
            s, news = query_news()
            if s:
                raise Exception(news)
            else:
                cursor = news[0]['n_cursor']
                returndata = news_to_json(True, cursor, news)
        except Exception, e:
            logger.error(str(e))
            returndata = json.dumps({'status' : '-100', 'content' : str(e)})
        finally:
            self.write(returndata)
            self.finish()

