#!/usr/bin/env python2.7
# Name: topic
# Function: post and read topic
# Date: 2016-06-07
# Email: day9011@gmail.com
__author__ = 'day9011'

from tornado.web import RequestHandler
import tornado
from lib.db import Mydb
from utils.news_log import getlogger
import json
from utils.post_valid import *
from utils.get_time import *

logger = getlogger()

__all__ = ['post_topic', 'get_topic', 'get_topic_list']

class post_topic(RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        ret = json.dumps({'status': 0, 'content': 'OK'})
        db = Mydb()
        try:
            info = self.request.protocol + "://" + self.request.host + ", method=" + self.request.method + ", access url=" + self.request.uri
            logger.info(info)
            body = self.request.body_arguments
            Args = [
                self_argument('username', required=True, helpinfo="miss user name"),
                self_argument('title', required=True, helpinfo="miss topic title"),
                self_argument('content', required=True, helpinfo="miss topic content"),
            ]
            s, vals = DataIsValid(Args, body)
            if s:
                raise Exception(vals)
            username = vals['username']
            if not(username):
                raise Exception("No username, Maybe not login")
            sql_str = "SELECT * FROM user WHERE username='%s'" % (username)
            s, f = db.get(sql_str)
            if s or not(f):
                raise Exception("No this user")
            title = vals['title']
            if len(title) > 100:
                raise Exception("title has too many words")
            content = vals['content']
            if len(content) < 100:
                abstract = content
            else:
                abstract = content[:100]
            date = get_ct()
            sql_str = "INSERT INTO topic VALUES (NULL, %s, %s, %s, %s, %s)"
            data = [username, title, content, abstract, date]
            s, f = db.modify(sql_str, data)
            if s:
               raise Exception(f)
        except Exception, e:
            logger.error(str(e))
            ret = json.dumps({'status': '-120', 'content': str(e)})
        finally:
            self.write(ret)
            self.finish()

class get_topic_list(RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        try:
            info = self.request.protocol + "://" + self.request.host + ", method=" + self.request.method + ", access url=" + self.request.uri
            logger.info(info)
            ret = ""
            c_cursor = ""
            pre = False
            db = Mydb()
            topics = []
            s, min_cursor = db.get('SELECT min(topic_id) as min_cursor FROM topic')
            if s:
                raise Exception("cant get max cursor")
            else:
                min_cursor = min_cursor[0]['min_cursor']
            try:
                c_cursor = int(self.get_argument('cursor'))
                num_news = int(self.get_argument('num'))
            except:
                logger.error('get cursor or num error')
                raise Exception('get cursor or num error')
            if c_cursor < 1:
                sql_str = 'SELECT topic_id as n_cursor, username as author, title as title, abstract as abstract,' \
                          'commit_time as commit_time FROM topic ORDER BY topic_id DESC LIMIT %s' % (str(num_news))
                s, comments = db.get(sql_str)
                if s:
                    raise Exception("cant get comments data")
                cursor = comments[len(comments) - 1]['n_cursor']
                if int(cursor) == int(min_cursor):
                    pre = True
                ret = topic_to_json(pre, cursor, comments)
            else:
                sql_str = 'SELECT COUNT(*) as nums FROM topic WHERE topic_id<%d' % (c_cursor)
                s, num = db.get(sql_str)
                if s:
                    raise Exception(num)
                num = num[0]['nums']
                if num < 1:
                    raise Exception("no topics")
                if int(min_cursor) >= int(c_cursor):
                    ret = topic_to_json(True, min_cursor, [])
                else:
                    sql_str = 'SELECT topic_id as n_cursor, username as author, title as title, abstract as abstract,' \
                              'commit_time as commit_time FROM topic WHERE topic_id<=%d ORDER BY topic_id DESC LIMIT ' % (c_cursor)
                    if int(num) < int(num_news):
                        sql_str += str(num)
                        s, topics = db.get(sql_str)
                        if s:
                            raise Exception("cant get topics data")
                        cursor = topics[len(topics) - 1]['n_cursor']
                        ret = topic_to_json(True, cursor, topics)
                    else:
                        sql_str += str(num_news)
                        s, topics = db.get(sql_str)
                        if s:
                            raise Exception("cant get max topics data")
                        cursor = topics[len(topics) - 1]['n_cursor']
                        if int(cursor) == int(min_cursor):
                            pre = True
                        ret = topic_to_json(pre, cursor, topics)
        except Exception, e:
            logger.error(str(e))
            ret = json.dumps({'status': '-120', 'content': str(e)})
        finally:
            self.write(ret)
            self.finish()

class get_topic(RequestHandler):
    @tornado.web.asynchronous
    def get(self, id):
        db = Mydb()
        ret = json.dumps({'status': 0, 'content': 'OK'})
        err = False
        try:
            info = self.request.protocol + "://" + self.request.host + ", method=" + self.request.method + ", access url=" + self.request.uri
            logger.info(info)
            info = "get %s topic" % (str(id))
            logger.info(info)
            sql_str = 'SELECT title, content FROM topic WHERE topic_id=%s' % (str(id))
            s, topic_dict = db.get(sql_str)
            if s or not topic_dict:
                err = True
                raise Exception(str(topic_dict))
            topic_dict = topic_dict[0]
        except Exception, e:
            logger.error(str(e))
            ret = json.dumps({'status': '-120', 'content': str(e)})
        finally:
            if err:
                self.write(ret)
                self.finish()
            else:
                self.render('topic.html', title=topic_dict['title'], content=topic_dict['content'], topic_id=str(id))

def topic_to_json(pre, cursor, topics):
    jsonstr = '{'
    jsonstr += '"pre": %s,' % (str(pre).lower())
    jsonstr += '"current_cursor": %d,' % (cursor)
    if topics == []:
        jsonstr += '"topics": []'
    else:
        jsonstr += '"topics":['
    for item in topics:
        item['id'] = item['n_cursor']
        item['commit_time'] = item['commit_time'].strftime("%Y-%m-%d %H:%M:%S")
        item.pop('n_cursor')
        jsonstr += json.dumps(item) + ','
    jsonstr = jsonstr[:-1]
    jsonstr += ']}'
    return jsonstr
