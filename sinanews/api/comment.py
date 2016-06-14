#!/usr/bin/env python2.7
#coding=utf-8
# Name: comment
# Function: comment api
# Date: 2016-06-14
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

class post_comment(RequestHandler):
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
                self_argument('topic_id', required=True, helpinfo="miss topic id"),
                self_argument('content', required=True, helpinfo="miss comment content"),
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
            date = get_ct()
            content = vals['content']
            topic_id = vals['topic_id']
            sql_str = "SELECT * FROM topic WHERE topic_id=%s" % (topic_id)
            s, f= db.get(sql_str)
            if s or not(f):
                raise Exception("No this topic")
            sql_str = "INSERT INTO comment VALUES (NULL, %s, %s, %s, %s)"
            data = [username, topic_id, content, date]
            s, f = db.modify(sql_str, data)
            if s:
                raise Exception(f)
        except Exception, e:
            logger.error(str(e))
            ret = json.dumps({'status': '-120', 'content': str(e)})
        finally:
            self.write(ret)
            self.finish()


class get_comments(RequestHandler):
    @tornado.web.asynchronous
    def get(self, id):
        try:
            info = self.request.protocol + "://" + self.request.host + ", method=" + self.request.method + ", access url=" + self.request.uri
            logger.info(info)
            ret = ""
            c_cursor = ""
            pre = False
            db = Mydb()
            sql_str = 'SELECT COUNT(*) as nums FROM comment WHERE topic_id=%s' % (str(id))
            s, num = db.get(sql_str)
            if s:
                raise Exception(num)
            num = num[0]['nums']
            if num < 1:
                raise Exception("no comments")
            comments = []
            s, max_cursor = db.get('SELECT max(id) as max_cursor FROM comment WHERE topic_id=%s' % (str(id)))
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
                ret = comment_to_json(True, max_cursor, [], num)
            else:
                sql_str = 'SELECT topic_id as n_cursor, username as author, content as content,' \
                          'commit_time as commit_time FROM comment WHERE id>%s and topic_id=%s ORDER BY commit_time LIMIT ' % (str(c_cursor), str(id))
                if num < num_news:
                    sql_str += str(num)
                    s, comments = db.get(sql_str)
                    if s:
                        raise Exception("cant get comments data")
                    cursor = comments[len(comments) - 1]['n_cursor']
                    ret = comment_to_json(True, cursor, comments, num)
                else:
                    sql_str += str(num_news)
                    print sql_str
                    s, comments = db.get(sql_str)
                    if s:
                        raise Exception("cant get max comments data")
                    cursor = comments[len(comments) - 1]['n_cursor']
                    if int(cursor) == int(max_cursor):
                        pre = True
                    ret = comment_to_json(pre, cursor, comments, num)
        except Exception, e:
            logger.error(str(e))
            ret = json.dumps({'status': '-120', 'content': str(e)})
        finally:
            self.write(ret)
            self.finish()

def comment_to_json(pre, cursor, comments, num):
    jsonstr = '{'
    jsonstr += '"pre": %s,' % (str(pre).lower())
    jsonstr += '"nums": %s,' % (str(num))
    jsonstr += '"current_cursor": %d,' % (cursor)
    if comments == []:
        jsonstr += '"comments": []'
    else:
        jsonstr += '"comments":['
    for item in comments:
        item['id'] = item['n_cursor']
        item['commit_time'] = item['commit_time'].strftime("%Y-%m-%d %H:%M:%S")
        item.pop('n_cursor')
        jsonstr += json.dumps(item) + ','
    jsonstr = jsonstr[:-1]
    jsonstr += ']}'
    return jsonstr