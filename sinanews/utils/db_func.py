#!/usr/bin/env python2.7
# Name: db_func
# Function: database operation
# Date: 2016-05-27
# Email: day9011@gmail.com
__author__ = 'day9011'

from lib import *
from news_log import getlogger

__all__ = ['insert_news', 'query_news']

logger = getlogger()
db = Mydb()

def insert_news(news):
    sql_if_exist_id = db.get('SELECT * FROM news_detail WHERE news_id = "%s"' % (news.data['id']))
    if not sql_if_exist_id:
        logger.error('this id is exists')
        return -3, 'this id is exists'
    sql_str = 'INSERT INTO news_detail VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    insert_info = [news.data['id'], news.data['url'], news.data['date'], news.data['source'], news.data['title'], news.data['content'], news.data['abstract'], news.data['keywords'], news.data['image']]
    try:
        s, f = db.modify(sql_str, insert_info)
        if s:
            raise Exception(f)
        logger.info("insert successfully id:" + news.data['id'])
        return 0, f
    except Exception, e:
        logger.error(str(e))
        return -10, str(e)

def query_news(*args):
    def query_news1(num = 0):
        sqlstr = 'SELECT news_cursor as n_cursor, news_source as source, news_url as url, news_keywords as keywords, ' \
                 'news_title as title, news_date as date, news_abstract as abstract, news_image as image, news_id as' \
                 ' id FROM news_detail ORDER BY news_cursor desc LIMIT '
        try:
            if num == 0:
                sqlstr += '20;'
                s, results = db.get(sqlstr)
            elif isinstance(num, int):
                sqlstr += str(num)
                s, results = db.get(sqlstr)
            else:
                return -4, 'need a int variable'
            if s:
                raise Exception("get data error by limit " + str(num) + "failed")
            return 0, results
        except Exception, e:
            logger.error(str(e))
            return -10, str(e)
    def query_news2():
        sqlstr = 'SELECT news_cursor as n_cursor, news_source as source, news_url as url, news_keywords as keywords, ' \
                 'news_title as title, news_date as date, news_abstract as abstract, news_image as image, news_id as' \
                 ' id FROM news_detail ORDER BY news_cursor desc LIMIT 30;'
        try:
            s, results = db.get(sqlstr)
            if s:
                raise Exception("cannot get default 30 latest news data")
            return 0, results
        except Exception, e:
            logger.error(str(e))
            return -10, str(e)
    #print "start query"
    if len(args) > 0:
        # print "It's in 1"
        return query_news1(*args)
    else:
        # print "It's in 2"
        return query_news2()

if __name__ == '__main__':
    s, result = query_news()
    print s, result